from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Type,
    TypeVar,
    Union,
    get_type_hints,
    overload,
)

import functools

from conjector.config_handler import ConfigHandler
from conjector.dtos import DEFAULT, Settings
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
        lazy_properties: Dict[str, Any] = {}
        setattr(
            cls,
            "init_props",
            lambda obj=cls, override_init=True: self._init_props(
                lazy_properties, obj, override_init=override_init
            ),
        )
        for class_var, type_ in get_type_hints(cls).items():
            value = config.get(class_var)
            if settings.type_cast:
                value = self._type_converter.cast_types(type_, value)
            lazy_properties[class_var] = value
        if not settings.lazy_init:
            self._init_props(
                lazy_properties, cls, override_init=settings.override_default
            )
        return cls

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
    filename: str = DEFAULT,
    override_default: bool = DEFAULT,
    root: str = DEFAULT,
    type_cast: bool = DEFAULT,
    lazy_init: bool = DEFAULT,
) -> Union[Callable[[Type[_T]], Type[_T]], Type[_T]]:
    """
    Decorator to inject config file values into class variables and cast them
    according to type hints.

    Parameters
    ----------
    cls:
        Class to inject constants. Passed implicit when decorator is used with
        or without parenthesis.
    filename:
        Name of file with constants. `yaml` and `json` formats are fully
        supported. `toml` and `ini` are supported but with some limitations.
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
    def wrapper(cls_: Type[_T]) -> Type[_T]:
        conjector = Conjector()
        return conjector.inject_config(
            cls_,
            settings=Settings(
                filename=filename,
                override_default=override_default,
                root=root,
                type_cast=type_cast,
                lazy_init=lazy_init,
            ),
        )

    if cls is None:
        return wrapper
    return wrapper(cls)
