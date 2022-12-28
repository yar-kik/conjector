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

from app_properties.config_handler import ConfigHandler
from app_properties.type_converter import TypeConverter

_T = TypeVar("_T")


class Conjector:
    def __init__(self) -> None:
        self._type_converter = TypeConverter()
        self._config_handler = ConfigHandler()

    def inject_config(
        self,
        cls: Type[_T],
        filename: str = "application.yml",
        ignore_case: bool = True,
        override_default: bool = False,
        root: str = "",
        type_cast: bool = True,
        lazy_init: bool = False,
    ) -> Type[_T]:
        config = self._config_handler.get_config(
            filename, ignore_case=ignore_case, root=root
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
            value = config.get(class_var.lower() if ignore_case else class_var)
            if type_cast:
                value = self._type_converter.cast_types(type_, value)
            lazy_properties[class_var] = value
        if not lazy_init:
            self._init_props(
                lazy_properties, cls, override_init=override_default
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


@overload
def properties(
    cls: None = None,
    *,
    filename: str = ...,
    ignore_case: bool = ...,
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
    ignore_case: bool = ...,
    override_default: bool = ...,
    root: str = ...,
    type_cast: bool = ...,
    lazy_init: bool = ...,
) -> Type[_T]:
    ...


def properties(
    cls: Optional[Type[_T]] = None,
    *,
    filename: str = "application.yml",
    ignore_case: bool = True,
    override_default: bool = False,
    root: str = "",
    type_cast: bool = True,
    lazy_init: bool = False,
) -> Union[Callable[[Type[_T]], Type[_T]], Type[_T]]:
    """
    Decorator to inject config file values into class variables and cast them
    according to type hints.

    :param cls: class to inject constants. Passed implicit when decorator
    is used with or without parenthesis.
    :param filename: name of file with constants. `yaml` and `json` formats are
    fully supported. `toml` is supported but with some limitations. Config file
    will be searched in the same directory where is file with used decorator.
    :param ignore_case: ignore case for field names or not.
    :param override_default: override default class vars or stay as is.
    :param root: for nested config - field names separated with dots, like
    `some.nested.key`.
    :param type_cast: apply type cast or stay as is.
    :param lazy_init: inject constants immediately or lazy. If lazy - method
    `init_props` should be called when necessary. This method also accept
    boolean keyword param `override_init` to keep values of initialized class
    or override them with config values.

    :return: class with injected constants.
    """

    @functools.wraps(cls)  # type: ignore
    def wrapper(cls_: Type[_T]) -> Type[_T]:
        conjector = Conjector()
        return conjector.inject_config(
            cls_,
            filename=filename,
            ignore_case=ignore_case,
            override_default=override_default,
            root=root,
            type_cast=type_cast,
            lazy_init=lazy_init,
        )

    if cls is None:
        return wrapper
    return wrapper(cls)
