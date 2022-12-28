# Python Config Injector
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/conjector)](https://pypi.org/project/conjector/)
[![PyPI - Package Version](https://img.shields.io/pypi/v/conjector)](https://pypi.org/project/conjector/)
[![PyPI - License](https://img.shields.io/pypi/l/conjector)](https://pypi.org/project/conjector/)
[![Build Status](https://app.travis-ci.com/yar-kik/conjector.svg?branch=master)](https://app.travis-ci.com/yar-kik/conjector)
[![Coverage Status](https://coveralls.io/repos/github/yar-kik/conjector/badge.svg?branch=master)](https://coveralls.io/github/yar-kik/conjector?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


## What is this
It is a simple library to inject non-sensitive configurations into class variables.
Basically, it's like `BaseSettings` in `pydantic` library but for constants in `json`, `yaml` or `toml` formats.
`conjector` can work with different Python types (like `tuple`, `datetime`, `dataclass` and so on) and recursively cast config values to them. 

## When to use
* If you deal with constants in your code, like error messages, default values for something, numeric coefficients, and so on.
* If you hate global variables, and you like non-python files to store static information.
* If you want to have an easy way to manage different constants depending on environments (like `test`, `dev`, `prod`).
* If you like type hints and clean code.

## How to install
To install this library just enter:
```shell
pip install conjector
```
By default, `conjector` work only with the builtin `json` deserializer.
To work with `yaml` or `toml` (if you are using `python <= 3.10`):
```shell
pip install conjector[yaml]
# or
pip install conjector[toml]
# or faster version of json
pip install conjector[json]
```

## How to use
For injecting values you need only the decorator `properties` under a target class.
By default, the library will search a config file `application.yml` in the same directory 
where your file with the used decorator is located, like below:

```
project_root
|---services
|   |   email_message_service.py
|   |   application.yml
|.....
```

Example:

`services/application.yml`:

```yaml 
default_text_style:
  size: 14
  weight: bold
  font: "Times New Roman"
  color:
    - 128
    - 128
    - 128
language_greetings:
  - language: english
    text: hello
  - language: german
    text: hallo
  - language: french
    text: bonjour
wellcome_message: "{greeting}! Thank you for registration, {username}!"
mailing_frequency:
  days: 5
  hours: 12
```
`services/email_message_service.py`:
```python
from typing import TypedDict
from dataclasses import dataclass
from datetime import timedelta
from app_properties import properties

@dataclass
class TextStyle:
    size: int
    weight: str
    font: str
    color: tuple[int, int, int] | str

class GreetingDict(TypedDict):
    language: str
    text: str

@properties
class EmailMessageService:
    default_text_style: TextStyle
    language_greetings: list[GreetingDict]
    wellcome_message: str
    mailing_frequency: timedelta | None
    
    # And using these class variables in some methods...
```

And that's how will look an equivalent of the code above but with "hard-coded" constants, without config files and `@properties` decorator:
```python
class EmailMessageService:
    default_text_style = TextStyle(
        size=14, weight="bold", font="Times New Roman", color=(128, 128, 128)
    )
    language_greetings = [
      GreetingDict(language="english", text="hello"),
      GreetingDict(language="german", text="hallo"),
      GreetingDict(language="french", text="bonjour"),
    ]
    wellcome_message = "{greeting}! Thank you for registration, {username}!"
    mailing_frequency = timedelta(days=5, hours=12)
    
    # And using these class variables in some methods...
```

All config values will be inserted and cast according to the type annotations once during the application or script start.
Additionally, the decorator takes such params:
* `filename` - the name of a file with config. By default, it is `application.yml`. Use a relative path with `../` to read the file from a parent directory;
* `type_cast` - used to know whether you want to cast config values to the field type. 
By default, it's `True`, which means values in a config file will be cast according to the type hints. All types specified in the section `supported types` will be available for type casting. Also, nested types will be recursively cast.
If `False`, type hinting is ignored, and available types are limited by a file format;
* `override_default` - used to know whether you want to override the default values of class variables. By default, it is `False`;
* `lazy_init` - used to know whether you want to set config values immediately on the application start-up or on demand ("lazily") after calling the method `init_props()`. By default, it is `False`;
* `root` - root key in the config. It's the way to create "namespaces" when you work with multiple classes but use a single config file. It could be a nested value with separation by dots, for example:
```yaml
# example.yml
services:
  email_service:
    key: some value
  auth_service:
    key: another value

clients:
  translation_client:
    key: value

# and so on...
```
```python
from app_properties import properties

@properties(filename="example.yml", root="services.email_service")
class EmailService:
    key: str  # will store "some value"


@properties(filename="example.yml", root="services.auth_service")
class AuthService:
    key: str  # will store "another value"
```
## Different environments
Using this library it's easy to manage different environments and corresponding config files.
It could be done like so:

```python
import os
from app_properties import properties


@properties(filename=os.getenv("CONFIG_FILENAME", "application.yml"))
class SomeEnvDependingService:
    env_depend_var: str
```
In this case, you set `CONFIG_FILENAME=application-dev.yml` in env variables, and `conjector` will use that file.

## Lazy initialization
If you want to create some dataclass instance with filled required data during init, 
and then populated with config values, you can use the parameter `lazy_init` for this purpose.
All file constants will be injected after calling the method `init_props`:
```python
# All definitions like in previous examples

@properties(lazy_init=True)
@dataclass
class EmailMessageServiceConfig:
    default_text_style: TextStyle
    language_greetings: list[GreetingDict]
    mailing_frequency: timedelta | None = None
    wellcome_message: str = "some_default_message"

email_config = EmailMessageServiceConfig(
    default_text_style=TextStyle(
        size=16, weight="normal", font="Arial", color="black"
    ),
    language_greetings=[GreetingDict(language="english", text="hello")]
)
# it works like a normal dataclass instance
assert email_config.default_text_style == TextStyle(
    size=16, weight="normal", font="Arial", color="black"
)
assert email_config.mailing_frequency is None
assert email_config.wellcome_message == "some_default_message"

# after calling `init_props`, config values will be injected. 
# It also overrides all values that we set during initialize before.
email_config.init_props()
assert email_config.default_text_style == TextStyle(
    size=14, weight="bold", font="Times New Roman", color=(128, 128, 128)
)
assert email_config.mailing_frequency == timedelta(days=5, hours=12)
assert email_config.wellcome_message == (
    "{greeting}! Thank you for registration, {username}!"
)
```

Because there are 3 sources of data (default values, values passed during initialization, and config file values), 
it could be hard to understand how we can resolve this conflict.
Bellow is the table to clarify the behavior of the `init_props` method.

| init     | default | config | will be used  |
|----------|---------|--------|---------------|
| -        | +       | -      | default       |
| -        | +       | +      | config        |
| +        | ~       | -      | init          |
| +        | ~       | +      | init \ config |

_`+`- provided; `-`- missing; `~`- not affect._

How you can see, when both `init` and `config` values provided, they are equally important,
but, by default, `config` have higher priority and overrides `init`. 
If you, for some reason, don't want to override already initialized values, only defaults,
it's also possible with `init_props(override_init=False)`

## Supported types
The table below shows how config values (`json` syntax example) are cast to Python types:

| Python type                                  | Config file type                      | Config example                                                                                                                                                 |
|----------------------------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `int`                                        | `int`<br/>`str`                       | `10`<br/>`"10"`                                                                                                                                                |
| `float`                                      | `float`<br/>`int`<br/>`str`           | `10.5`<br/>`10`<br/>`"10.5"`                                                                                                                                   |
| `str`                                        | `str`                                 | `"string value"`                                                                                                                                               |
| `bool`                                       | `bool`<br/>`int`<br/>`str`            | `true` / `false`<br/>`1` / `0`<br/>`"True"` / `"False"`, `"true"` / `"false"`                                                                                  |
| `None`                                       | `null`                                | `null`                                                                                                                                                         |
| `dict`                                       | `dict`                                | `{"key": "value"}`                                                                                                                                             |
| `list`<br/>`tuple`<br/>`set`<br/>`frozenset` | `list`                                | `["val1", "val2"]`                                                                                                                                             |
| `TypedDict`                                  | `dict`                                | `{"str_var": "value"}`                                                                                                                                         |
| `NamedTuple`                                 | `list`<br/>`dict`                     | `["value", 10]`<br/>`{"str_val": "value", "int_val": 10}`                                                                                                      |
| `dataclass`                                  | `dict`                                | `{"str_val": "str", "int_val": 10}`                                                                                                                            |
| `datetime.datetime`                          | `str`<br/>`int`<br/>`list`<br/>`dict` | `"2022-12-11T10:20:23"`<br/>`1670754600`<br/>`[2022, 12, 11, 10, 20, 23]`<br/>`{"year": 2022, "month": 12, "day": 11, "hour": 10, "minute": 20, "second": 23}` |
| `datetime.date`                              | `str`<br/>`list`<br/>`dict`           | `"2022-12-11"`<br/>`[2022, 12, 11]`<br/>`{"year": 2022, "month": 12, "day": 11}`                                                                               |
| `datetime.time`                              | `str`<br/>`list`<br/>`dict`           | `"12:30:02"`<br/>`[12, 30, 2]`<br/>`{"hour": 12, "minute": 30, "second": 2}`                                                                                   |
| `datetime.timedelta`                         | `dict`                                | `{"days": 1, "hours": 2, "minutes": 10}`                                                                                                                       |
| `enum.Enum`                                  | `str`<br/>`int`                       | `"VALUE"`<br/>`10`                                                                                                                                             |
| `re.Pattern`                                 | `str`                                 | `"\w+"`                                                                                                                                                        |

___Warning:___ `toml` config format doesn't support heterogeneous types in an array, 
like `["string", 10]`. So, using iterables with mixed types 
(e.g. `list[str | int]` or `tuple[str, int]`) and corresponding type casting 
aren't possible in this case.

## About contributing
You will make `conjector` better if you open issues or create pull requests with improvements.