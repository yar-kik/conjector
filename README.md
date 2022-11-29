# Python Application Properties
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-app-properties)](https://pypi.org/project/py-app-properties/)
[![PyPI - Package Version](https://img.shields.io/pypi/v/py-app-properties)](https://pypi.org/project/py-app-properties/)
[![PyPI - License](https://img.shields.io/pypi/l/py-app-properties)](https://pypi.org/project/py-app-properties/)
[![Build Status](https://app.travis-ci.com/yar-kik/py-app-properties.svg?branch=master)](https://app.travis-ci.com/yar-kik/py-app-properties)
[![Coverage Status](https://coveralls.io/repos/github/yar-kik/py-app-properties/badge.svg?branch=master)](https://coveralls.io/github/yar-kik/py-app-properties?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)


## What is this
This is a simple library to inject non-sensitive configurations into class variables.

## How to install
To install this library just enter:
```shell
pip install py-app-properties
```

## How To Use
The main purpose of this library is to simplify work with an application config. 
Using decorator `@properties` with all required params and type hinting you can inject required settings from `*.yml` or `*.json` formats.

Example:
```yaml 
# my_app_properties.yml
my_class:
  int_var: 10
  list_int_var:
    - 12
    - 14
  dict_with_list_var:
    key1:
      - val1
      - val2
    key2:
      - val3
      - val4
  bool_var: true
```
```python
from app_properties import properties

@properties(filename="my_app_properties.yml", root="my_class")
class MyClass:
    int_var: int
    list_int_var: list[int]
    dict_with_list_var: dict[str, list[str]]
    bool_var: bool
    
    def __init__(self, param1: int, param2: str) -> None:
        self._param1 = param1
        self._param2 = param2
    
    def some_method(self) -> None:
        ...  # using class variables and instance variables here
```
About params:
* `filename` - the name of a file with config. By default, it is `application.yml` which is located in the same directory as a file with a used decorator. Use a relative path with `../` to read the file from a parent directory.
* `type_cast` - used to know whether you want to cast config values to field type. 
By default, it's `True`, which means values in a config file will be cast according to the type hints. 
If `False`, type hinting is ignored, and available types are limited by a file format - only `list`, `dict`, `int`, `str`, `float`, `bool`, and `none` are available.
If `True` - `set`, `frozenset`, `tuple`, `NamedTuple`, `TypedDict`, and `dataclass` will be available additionally to types above. Also nested types will be recursively cast.
* `override_default` - used to know whether you want to override default values of class variables. By default, it is `False`.
* `root` - root key in the config. Could be a nested value with separation by dots, for example:
```yaml
# example.yml
some:
  nested:
    config:
      key: value
```
```python
@properties(filename="example.yml", root="some.nested.config")
class MyClass:
    key: str
```
## About contributing
You will make this library better if you open issues or create pull requests with improvements.