from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

import decimal
import enum
import inspect
import pathlib
import re
from collections.abc import Iterable, Mapping
from dataclasses import MISSING, Field, fields, is_dataclass
from datetime import date, datetime, time, timedelta
from itertools import zip_longest


class TypeConverter:
    _primitive_types = (
        str,
        int,
        float,
        bool,
        type(None),
        enum.Enum,
        decimal.Decimal,
        pathlib.Path,
    )
    _boolean_map = {
        "true": True,
        "True": True,
        "1": True,
        "false": False,
        "False": False,
        "0": False,
    }

    def cast_types(self, type_: Union[Type, Any], value: Any) -> Any:
        args = args if (args := get_args(type_)) else (Any,)
        type_ = origin if (origin := get_origin(type_)) else type_
        value = value if value != "null" else None
        if (
            self._is_unspecified(type_)
            or self._is_terminate(type_, args)
            and isinstance(value, type_)
        ):
            return value
        if self._is_union(type_):
            return self._apply_union(args, value)
        if issubclass(type_, Mapping):
            return self._cast_mapping(type_, args, value)
        if issubclass(type_, Iterable):
            return self._cast_iterable(type_, args, value)
        if self._is_datetime(type_):
            return self._apply_datetime(type_, value)
        if is_dataclass(type_):
            return self._apply_dataclass(type_, value)
        return self._cast_base(type_, value)

    def _cast_iterable(self, type_: type, args: tuple, value: Any) -> Any:
        if type_ == str:
            return self._cast_base(type_, value)
        if type_ == list:
            return self._apply_list(args, value)
        if issubclass(type_, tuple):
            return self._apply_tuple(type_, args, value)
        if type_ in (set, frozenset):
            return self._apply_set(type_, args, value)
        raise ValueError("Unsupported iterable type was found!")

    def _cast_mapping(self, type_: type, args: tuple, value: Any) -> Any:
        if issubclass(type_, dict):
            return self._apply_dict(type_, args, value)
        raise ValueError("Unsupported mapping type was found!")

    def _cast_base(self, type_: Type, value: Any) -> Any:
        if self._is_none_type(type_):
            return None
        if type_ == bool:
            return self._cast_bool(value)
        if type_ == re.Pattern:
            return self._apply_regex_pattern(value)
        if issubclass(type_, enum.Enum):
            return self._apply_enum(type_, value)
        if type_ == decimal.Decimal:
            return self._apply_decimal(value)
        if type_ == pathlib.Path:
            return self._apply_path(value)
        if value is None:
            return type_()
        return type_(value)

    def _cast_bool(self, value: Any) -> Optional[bool]:
        if value is None:
            return bool()
        if isinstance(value, bool):
            return value
        return self._boolean_map.get(str(value))

    def _apply_list(self, args: Tuple[Type[list], ...], values: Any) -> list:
        if values is None:
            values = list()
        return [self.cast_types(args[0], i) for i in values]

    def _apply_set(
        self, type_: type, args: Tuple[Type[set], ...], values: Any
    ) -> set:
        if values is None:
            values = set()
        return type_(self.cast_types(args[0], i) for i in values)

    def _apply_tuple(
        self, type_: Type[tuple], args: Any, values: Any
    ) -> tuple:
        if values is None:
            values = tuple()
        if not get_type_hints(type_):
            args = (Any, ...) if self._is_any(args) else args
            args = self._resolve_ellipsis(args, values)
            cast_values: Any = [
                self.cast_types(arg, value) for arg, value in zip(args, values)
            ]
            return tuple(cast_values)
        if isinstance(values, Mapping):
            cast_values = {}
            for field, arg in get_type_hints(type_).items():
                cast_values[field] = self.cast_types(arg, values.get(field))
            return type_(**cast_values)
        if isinstance(values, Iterable):
            cast_values = []
            for arg, value in zip_longest(
                get_type_hints(type_).values(), values
            ):
                cast_values.append(self.cast_types(arg, value))
            return type_(*cast_values)
        raise ValueError("NamedTuple values should be iterable or mapping!")

    def _apply_dict(self, type_: Type[dict], args: tuple, values: Any) -> dict:
        if values is None:
            values = dict()
        if not isinstance(values, dict):
            raise ValueError(f"Value '{values}' isn't mapping!")
        if not self._is_any(args):
            return {
                self.cast_types(args[0], k): self.cast_types(args[1], v)
                for k, v in values.items()
            }
        cast_values = {}
        for field, arg in get_type_hints(type_).items():
            cast_values[field] = self.cast_types(arg, values.get(field))
        return type_(**cast_values)

    def _apply_dataclass(self, type_: type, values: Any) -> Any:
        if values is None:
            values = dict()
        field_mapping = {}
        for field in fields(type_):
            if not field.init:
                continue
            default = self._get_dataclass_default(field)
            field_mapping[field.name] = self.cast_types(
                field.type, values.get(field.name, default)
            )
        return type_(**field_mapping)

    def _apply_datetime(
        self,
        type_: Union[Type[datetime], Type[date], Type[time], Type[timedelta]],
        values: Any,
    ) -> Union[datetime, date, time, timedelta]:
        if values is None:
            default_value = {
                datetime: datetime(year=1970, month=1, day=1),
                date: date(year=1970, month=1, day=1),
            }.get(type_)
            return default_value if default_value else type_()  # type: ignore
        if type_ == timedelta:
            if isinstance(values, Mapping):
                values = self.cast_types(Dict[str, int], values)
                return timedelta(**values)
            raise ValueError(f"Cannot cast value {values} to timedelta")
        if type_ == datetime and self._is_number(values):
            return datetime.utcfromtimestamp(float(values))
        if isinstance(values, str):
            return type_.fromisoformat(values)  # type: ignore
        if isinstance(values, Mapping):
            values = self.cast_types(Dict[str, int], values)
            return type_(**values)
        if isinstance(values, Iterable):
            values = self.cast_types(List[int], values)
            return type_(*values)
        raise ValueError(f"Cannot cast value {values} to {type_.__name__}!")

    def _get_dataclass_default(self, field: Field) -> Any:
        if field.default is not MISSING:
            return field.default
        if field.default_factory is not MISSING:
            return field.default_factory()
        return None

    def _resolve_ellipsis(
        self, args: Tuple[type, ...], values: Any
    ) -> Tuple[type, ...]:
        try:
            value_len = len(values)
        except TypeError:
            raise ValueError(f"Value {values} should be iterable!")
        if ... in args:
            return tuple(args[0] for _ in range(value_len))
        return args

    def _apply_union(self, args: Any, value: Any) -> Any:
        is_optional = type(None) in args
        if is_optional and value is None:
            return None
        args = [i for i in args if not self._is_none_type(i)]
        for arg in args:
            try:
                return self.cast_types(arg, value)
            except (ValueError, TypeError):
                continue
        if is_optional:
            return None
        raise ValueError(f"Couldn't cast '{value}' to any of types: {args}")

    def _apply_regex_pattern(self, values: Any) -> re.Pattern:
        if not isinstance(values, str):
            raise ValueError("Regex pattern should be string!")
        return re.compile(values)

    def _apply_enum(self, type_: Type[enum.Enum], values: Any) -> enum.Enum:
        if issubclass(type_, enum.IntEnum):
            return type_(int(values))
        return type_(values)

    def _apply_decimal(self, value: Any) -> decimal.Decimal:
        if value is None:
            return decimal.Decimal()
        if isinstance(value, list):
            if len(value) != 3:
                raise ValueError("Decimal value requires 3-items iterable!")
            value = self.cast_types(Tuple[int, List[int], int], value)
            return decimal.Decimal(value)
        if self._is_number(value):
            return decimal.Decimal(value)
        raise ValueError(
            "Decimal value should be int, float, str or 3-items list!"
        )

    def _apply_path(self, value: Any) -> pathlib.Path:
        if value is None:
            return pathlib.Path()
        if isinstance(value, str):
            return pathlib.Path(value)
        raise ValueError("Path constructor accept only string argument!")

    def _is_number(self, num: Any) -> bool:
        if isinstance(num, (int, float)):
            return True
        try:
            float(num)
            return True
        except (ValueError, TypeError):
            return False

    def _is_terminate(self, type_: Any, args: tuple) -> bool:
        return (
            self._is_any(args)
            and not self._is_primitive(type_)
            and not get_type_hints(type_)
        )

    def _is_primitive(self, type_: type) -> bool:
        return any(issubclass(type_, i) for i in self._primitive_types)

    def _is_none_type(self, arg: Any) -> bool:
        return inspect.isclass(arg) and issubclass(arg, type(None))

    def _is_any(self, args: Tuple[type, ...]) -> bool:
        return args == (Any,)

    def _is_unspecified(self, type_: Any) -> bool:
        return isinstance(type_, TypeVar) or type_ == Any

    def _is_datetime(self, type_: type) -> bool:
        return type_ in (datetime, date, time, timedelta)

    def _is_union(self, type_: type) -> bool:
        return type_ == Union or type_.__name__ == "UnionType"
