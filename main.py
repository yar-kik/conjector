import logging
from typing import Optional, TypeVar

import yaml
from functools import wraps
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
    conf = yaml.load(text_content, CSafeLoader)
    return {k.replace("-", "_"): v for k, v in conf.items()}


def inject_properties(
    cls: Optional[_CV] = None,
    /,
    *,
    filename: str = "application.yml",
    ignore_case: bool = True,
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
        if ignore_case:
            conf = {k.lower(): v for k, v in conf.items()}
        for class_var in annotated_class_vars:
            if class_var in default_class_vars:
                continue
            class_var_ = class_var.lower() if ignore_case else class_var
            val = conf.get(class_var_, None)
            setattr(obj, class_var, val)
        return obj

    if cls is None:
        return wrapper
    return wrapper(cls)
