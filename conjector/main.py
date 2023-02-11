from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    get_type_hints,
    overload,
)

import functools
import inspect

from conjector.config_handler import ConfigHandler
from conjector.entities import MISSING, Default, Settings
from conjector.type_converter import TypeConverter

_T = TypeVar("_T")


class Conjector:
    def __init__(self) -> None:
        self._type_converter = TypeConverter()
        self._config_handler = ConfigHandler()

    def inject_config(
        self, cls: Type[_T], settings: Optional[Settings] = None
    ) -> Type[_T]:
        settings = self._get_merged_settings(settings)
        config = self._config_handler.get_config(
            settings.filename, root=settings.root
        )
        cast_values = self._get_cast_config_values(
            config, get_type_hints(cls), settings.type_cast
        )
        self._inject_values_in_class(
            cls, cast_values, settings.lazy_init, settings.override_default
        )
        return cls

    def replace_defaults(
        self,
        func: Callable[..., _T],
        args: tuple,
        kwargs: dict,
        settings: Optional[Settings] = None,
    ) -> _T:
        settings = self._get_merged_settings(settings)
        config = self._config_handler.get_config(
            settings.filename, root=settings.root
        )
        type_hints = self._get_func_type_hints(func)
        cast_values = self._get_cast_config_values(
            config, type_hints, settings.type_cast
        )
        default_values = self._get_func_default_values(func)
        combined_values = self._combine_cast_and_default_values(
            cast_values, default_values, set(config.keys())
        )
        param = self._inject_values_in_func(
            func, combined_values, args, kwargs
        )
        return func(*param.args, **param.kwargs)

    def _inject_values_in_class(
        self,
        cls: Type[_T],
        cast_values: Dict[str, Any],
        lazy_init: bool,
        override_default: bool,
    ) -> None:
        setattr(
            cls,
            "init_props",
            lambda obj=cls, override_init=True: self._init_props(
                cast_values, obj, override_init=override_init
            ),
        )

        if not lazy_init:
            self._init_props(cast_values, cls, override_init=override_default)

    def _inject_values_in_func(
        self, func: Callable, values: Dict[str, Any], args: tuple, kwargs: dict
    ) -> inspect.BoundArguments:
        new_params = []
        func_params = inspect.signature(func).parameters
        for name, param in func_params.items():
            if self._is_override_default(param):
                param = param.replace(default=values.get(name))
            new_params.append(param)
        params = (
            inspect.signature(func)
            .replace(parameters=new_params)
            .bind(*args, **kwargs)
        )
        params.apply_defaults()
        return params

    def _combine_cast_and_default_values(
        self,
        cast_values: Dict[str, Any],
        default_values: Dict[str, Any],
        config_keys: Set[str],
    ) -> Dict[str, Optional[Any]]:
        values = {}
        for name in default_values:
            value = cast_values.get(name)
            if name not in config_keys:
                value = (
                    default_values[name]
                    if default_values[name] is not MISSING
                    else value
                )
            values[name] = value
        return values

    def _get_func_default_values(self, func: Callable) -> Dict[str, Any]:
        return {
            k: v.default.value
            for k, v in inspect.signature(func).parameters.items()
            if self._is_override_default(v)
        }

    def _get_func_type_hints(self, func: Callable) -> Dict[str, Any]:
        # method is required because `typing.get_type_hints` doesn't work on
        # function parameters without type annotation.
        return {
            k: Any if v.annotation is v.empty else v.annotation
            for k, v in inspect.signature(func).parameters.items()
            if self._is_override_default(v)
        }

    def _is_override_default(self, param: inspect.Parameter) -> bool:
        return param.default is not param.empty and isinstance(
            param.default, Default
        )

    def _get_cast_config_values(
        self,
        config: Dict[str, Any],
        type_hints: Dict[str, Any],
        type_cast: bool,
    ) -> Dict[str, Any]:
        cast_values = {}
        for class_var, type_ in type_hints.items():
            value = config.get(class_var)
            if type_cast:
                value = self._type_converter.cast_types(type_, value)
            cast_values[class_var] = value
        return cast_values

    @staticmethod
    def _init_props(
        lazy_properties: Dict[str, Any],
        obj: Optional[_T] = None,
        *,
        override_init: bool = True,
    ) -> None:
        for field, value in lazy_properties.items():
            if override_init and value:
                setattr(obj, field, value)
            else:
                if getattr(obj, field, None) is None:
                    setattr(obj, field, value)

    def _get_global_settings(self) -> Settings:
        cast_settings = {}
        raw_settings = self._config_handler.get_global_settings()
        for name, type_ in get_type_hints(Settings).items():
            if name in raw_settings:
                cast_settings[name] = self._type_converter.cast_types(
                    type_, raw_settings[name]
                )
        return Settings(**cast_settings)

    def _get_merged_settings(
        self, user_params: Optional[Settings]
    ) -> Settings:
        global_settings = self._get_global_settings()
        settings = user_params if user_params else Settings()
        return global_settings | settings


@overload
def properties(
    cls: None = None,
    *,
    filename: str = ...,
    override_default: bool = ...,
    root: str = ...,
    type_cast: bool = ...,
    lazy_init: bool = ...,
) -> Callable[[Type[_T]], Type[_T]]:
    ...


@overload
def properties(
    cls: Type[_T],
    *,
    filename: str = ...,
    override_default: bool = ...,
    root: str = ...,
    type_cast: bool = ...,
    lazy_init: bool = ...,
) -> Type[_T]:
    ...


def properties(
    cls: Optional[Type[_T]] = None,
    *,
    filename: str = Default("filename"),
    override_default: bool = Default(False),
    root: str = Default(""),
    type_cast: bool = Default(True),
    lazy_init: bool = Default(False),
) -> Union[
    Callable[[Type[_T]], Union[Type[_T], Callable[..., _T]]],
    Union[Type[_T], Callable[..., _T]],
]:
    """
    Decorator to inject config file values into class variables and cast them
    according to type hints.

    Parameters
    ----------
    cls:
        Class to inject constants. Passed implicit when decorator is used with
        or without parenthesis.
    filename:
        Name of file with constants. `yaml`, `json` and `toml` formats are
        fully supported. `ini` is supported but with some limitations.
        Config file will be searched in the same directory where is file with
        used decorator. Default value is **"application.yml"**
    override_default:
        Override default class vars or stay as is. Default is **False**
    root:
        For nested config - field names separated with dots, like
        `some.nested.key`. Default is **""**
    type_cast:
        Apply type cast or stay as is. Default is **True**
    lazy_init:
        Inject constants immediately or lazy. If lazy - method `init_props`
        should be called when necessary. This method also accept boolean
        keyword param `override_init` to keep values of initialized class or
        override them with config values. Default value is **False**

    Returns
    -------
    cls
        Class with injected constants.
    """

    @functools.wraps(cls)  # type: ignore
    def wrapper(cls_: Type[_T]) -> Union[Type[_T], Callable[..., _T]]:
        def argument_handler(*args: Any, **kwargs: Any) -> Any:
            return conjector.replace_defaults(cls_, args, kwargs, settings)

        if inspect.isfunction(cls_):
            return argument_handler
        return conjector.inject_config(cls_, settings=settings)

    conjector = Conjector()
    settings = Settings(
        filename=filename,
        override_default=override_default,
        root=root,
        type_cast=type_cast,
        lazy_init=lazy_init,
    )
    if cls is None:
        return wrapper
    return wrapper(cls)
