import json
import logging
from typing import Optional, TypeVar

import yaml
from functools import wraps, reduce
from pathlib import Path
from yaml import CSafeLoader

import inspect

_CV = TypeVar("_CV", bound=type)

logger = logging.getLogger(__name__)


def get_conf(conf_name: str) -> dict:
    file = Path(conf_name)
    if not file.exists():
        logger.warning(f"File {file} was not found. Using default values...")
        return {}
    text_content = file.read_text()
    if conf_name.endswith(".yml") or conf_name.endswith(".yaml"):
        conf = get_yaml_config(text_content)
    elif conf_name.endswith(".json"):
        conf = get_json_config(text_content)
    else:
        raise NotImplementedError("Specified config type isn't supported!")
    return {k.replace("-", "_"): v for k, v in conf.items()}


def get_yaml_config(text_content: str) -> dict:
    return yaml.load(text_content, CSafeLoader)


def get_json_config(text_content: str) -> dict:
    return json.loads(text_content)


def inject_properties(
    cls: Optional[_CV] = None,
    /,
    *,
    filename: str = "application.yml",
    ignore_case: bool = True,
    override_default: bool = False,
    root: str = "",
    cast: bool = False,
):
    @wraps(cls)
    def wrapper(obj) -> _CV:
        annotated_class_vars = obj.__annotations__
        default_class_vars = {
            k: v
            for k, v in inspect.getmembers(obj)
            if not (
                k.startswith("__")
                or callable(v)
                or isinstance(v, (property, classmethod))
            )
        }
        conf = get_conf(filename)
        if root:
            nested_path = root.split(".")
            conf = reduce(lambda x, y: x[y], nested_path, conf)
        if ignore_case:
            conf = {k.lower(): v for k, v in conf.items()}
        for class_var in annotated_class_vars:
            if not override_default and class_var in default_class_vars:
                continue
            class_var_ = class_var.lower() if ignore_case else class_var
            val = conf.get(class_var_)
            if cast:
                type_ = annotated_class_vars[class_var]
                if isinstance(type_, type):
                    val = type_(val) if val else type_()
            setattr(obj, class_var, val)
        return obj

    if cls is None:
        return wrapper
    return wrapper(cls)
