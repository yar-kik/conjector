from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Type,
    TypeVar,
    Union,
    get_origin,
    get_type_hints,
    overload,
)

import inspect
import json
import logging
import yaml
from functools import reduce, wraps
from pathlib import Path
from yaml import CSafeLoader

_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")

logger = logging.getLogger(__name__)


def get_config(conf_name: str) -> dict:
    file = Path(conf_name)
    if not file.exists():
        logger.warning(f"File {file} was not found. Using default values...")
        return {}
    text_content = file.read_text()
    if conf_name.endswith(".yml") or conf_name.endswith(".yaml"):
        conf = _get_yaml_config(text_content)
    elif conf_name.endswith(".json"):
        conf = _get_json_config(text_content)
    else:
        raise NotImplementedError("Specified config type isn't supported!")
    return conf


def _get_yaml_config(text_content: str) -> dict:
    return yaml.load(text_content, CSafeLoader)


def _get_json_config(text_content: str) -> dict:
    return json.loads(text_content)


@overload
def inject_properties(
    cls: None = None,
    *,
    filename: str = "application.yml",
    ignore_case: bool = True,
    override_default: bool = False,
    root: str = "",
    type_cast: bool = False,
) -> Callable[[Type[_T]], Type[_T]]:
    ...


@overload
def inject_properties(
    cls: Type[_T],
    *,
    filename: str = "application.yml",
    ignore_case: bool = True,
    override_default: bool = False,
    root: str = "",
    type_cast: bool = False,
) -> Type[_T]:
    ...


def inject_properties(
    cls: Optional[Type[_T]] = None,
    *,
    filename: str = "application.yml",
    ignore_case: bool = True,
    override_default: bool = False,
    root: str = "",
    type_cast: bool = False,
) -> Union[Callable[[Type[_T]], Type[_T]], Type[_T]]:
    @wraps(cls)  # type: ignore
    def wrapper(obj: Type[_T]) -> Type[_T]:
        annotated_class_vars = get_type_hints(obj)
        default_class_vars = _get_default_class_var(obj)
        config = _process_config(get_config(filename), ignore_case, root)
        for class_var, type_ in annotated_class_vars.items():
            if not override_default and class_var in default_class_vars:
                continue
            value = config.get(class_var.lower() if ignore_case else class_var)
            if type_cast:
                value = _cast_types(type_, value)
            setattr(obj, class_var, value)
        return obj

    if cls is None:
        return wrapper
    return wrapper(cls)


def _cast_types(type_: type, value: Any) -> Any:
    type_ = origin if (origin := get_origin(type_)) else type_
    if isinstance(type_, type):
        return type_(value) if value else type_()
    return value


def _apply_to_key(
    mapping: Dict[_K, _V], func: Callable[[_K], _T]
) -> Dict[_T, _V]:
    return {func(k): mapping[k] for k in mapping}


def _process_config(config: dict, ignore_case: bool, root: str) -> dict:
    config = _apply_to_key(config, lambda x: str.replace(x, "-", "_"))
    if ignore_case:
        config = _apply_to_key(config, str.lower)
    if root:
        config = reduce(lambda x, y: x[y], root.split("."), config)
    return config


def _get_default_class_var(obj: type) -> dict:
    return {
        k: v
        for k, v in inspect.getmembers(obj)
        if not (
            k.startswith("__")
            or callable(v)
            or isinstance(v, (property, classmethod))
        )
    }
