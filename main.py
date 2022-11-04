from functools import wraps
from pathlib import Path
from typing import TypeVar, Optional

import yaml
from yaml import CSafeLoader

_CV = TypeVar("_CV", bound=type)


def get_conf(conf_name: str):
    text_content = Path(conf_name).read_text()
    conf = yaml.load(text_content, CSafeLoader)
    return {k.replace("-", "_"): v for k, v in conf.items()}


def inject_properties(
    cls: Optional[_CV] = None, /, *,
    filename: str = "application.yml",
    ignore_case: bool = True
):
    @wraps(cls)
    def wrapper(obj) -> _CV:
        annotated_class_vars = obj.__annotations__
        default_class_vars = {
            k: v
            for k, v in obj.__dict__.items()
            if not (
                k.startswith("__") or
                callable(v) or
                isinstance(v, (property, classmethod))
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


@inject_properties()
class A:
    bool: str
    array: str = "str"
    NESTED_DICT: dict

    def __init__(self, par1: int, par2: str = ""):
        self._par1 = par1
        self._par2 = par2

    def method(self):
        print(self.bool, self.array, self.NESTED_DICT)

    @property
    def prop(self):
        return

    @classmethod
    def class_method(cls):
        return


if __name__ == '__main__':
    a = A(1)
    a.method()
