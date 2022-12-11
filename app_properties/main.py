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
    supported. Config file will be searched in the same directory where is file
    with used decorator.
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
        def init_props(
            self: Optional[_T] = None, *, override_init: bool = True
        ) -> None:
            # if obj is None than method was called as classmethod
            # else we work with instance object
            obj = cls_ if self is None else self
            for field, value in lazy_properties.items():
                if override_init and value:
                    setattr(obj, field, value)
                else:
                    if getattr(obj, field, None) is None:
                        setattr(obj, field, value)

        type_converter = TypeConverter()
        config = ConfigHandler(filename).get_config(ignore_case, root)
        annotated_class_vars = get_type_hints(cls_)
        lazy_properties: Dict[str, Any] = {}
        setattr(cls_, "init_props", init_props)
        for class_var, type_ in annotated_class_vars.items():
            value = config.get(class_var.lower() if ignore_case else class_var)
            if type_cast:
                value = type_converter.cast_types(type_, value)
            lazy_properties[class_var] = value
        if not lazy_init:
            init_props(override_init=override_default)
        return cls_

    if cls is None:
        return wrapper
    return wrapper(cls)
