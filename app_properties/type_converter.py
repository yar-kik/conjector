from typing import (
    Any,
    Optional,
    Tuple,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

import inspect
from collections.abc import Iterable, Mapping
from dataclasses import fields, is_dataclass
from itertools import zip_longest


class TypeConverter:
    def cast_types(self, type_: Union[type, Any], value: Any) -> Any:
        args = args if (args := get_args(type_)) else (Any,)
        type_ = origin if (origin := get_origin(type_)) else type_
        if (
            isinstance(type_, TypeVar)
            or type_ == Any
            or self._is_terminate(type_, args)
            and isinstance(value, type_)
        ):
            return value
        if type_ == Union or type_.__name__ == "UnionType":
            return self._apply_union(args, value)
        if issubclass(type_, list):
            return self._apply_list(args, value)
        if issubclass(type_, tuple):
            return self._apply_tuple(type_, args, value)
        if issubclass(type_, dict):
            return self._apply_dict(type_, args, value)
        if issubclass(type_, (set, frozenset)):
            return self._apply_set(type_, args, value)
        if is_dataclass(type_):
            return self._apply_dataclass(type_, value)
        return self._cast_base(type_, value)

    def _cast_base(self, type_: type, value: Any) -> Any:
        if value is None or self._is_none_type(type_):
            return type_()
        if type_ == bool:
            return self._cast_bool(value)
        return type_(value)

    def _cast_bool(self, value: Any) -> Optional[bool]:
        if isinstance(value, bool):
            return value
        value = str(value)
        if value in ("true", "True", "1"):
            return True
        if value in ("false", "False", "0"):
            return False
        return None

    def _apply_list(self, args: Tuple[type, ...], values: Any) -> list:
        if values is None:
            values = list()
        return [self.cast_types(args[0], i) for i in values]

    def _apply_set(
        self, type_: type, args: Tuple[type, ...], values: Any
    ) -> set:
        if values is None:
            values = set()
        return type_(self.cast_types(args[0], i) for i in values)

    def _apply_tuple(self, type_: type, args: Any, values: Any) -> tuple:
        if values is None:
            values = tuple()
        if not get_type_hints(type_):
            args = (Any, ...) if self._is_unspecified(args) else args
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

    def _apply_dict(self, type_: type, args: tuple, values: Any) -> dict:
        if values is None:
            values = dict()
        if not isinstance(values, dict):
            raise ValueError("Value isn't mapping!")
        if not self._is_unspecified(args):
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
            field_mapping[field.name] = self.cast_types(
                field.type, values.get(field.name)
            )
        return type_(**field_mapping)

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
            except ValueError:
                continue
        if is_optional:
            return None
        raise ValueError(f"Couldn't cast '{value}' to any of types: {args}")

    def _is_terminate(self, type_: Any, args: tuple) -> bool:
        return (
            self._is_unspecified(args)
            and not self._is_primitive(type_)
            and not get_type_hints(type_)
        )

    def _is_primitive(self, type_: type) -> bool:
        return type_ in (str, int, float, bool, type(None))

    def _is_none_type(self, arg: Any) -> bool:
        return inspect.isclass(arg) and issubclass(arg, type(None))

    def _is_unspecified(self, args: Tuple[type, ...]) -> bool:
        return args == (Any,)
