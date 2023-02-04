# Python Config Injector
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/conjector)](https://pypi.org/project/conjector/)
[![PyPI - Package Version](https://img.shields.io/pypi/v/conjector)](https://pypi.org/project/conjector/)
[![PyPI - License](https://img.shields.io/pypi/l/conjector)](https://pypi.org/project/conjector/)
[![Documentation Status](https://readthedocs.org/projects/conjector/badge/?version=latest)](https://conjector.readthedocs.io/en/latest/?badge=latest)
[![Build](https://github.com/yar-kik/conjector/actions/workflows/package_build.yml/badge.svg?branch=master)](https://github.com/yar-kik/conjector/actions/workflows/package_build.yml)
[![Coverage Status](https://coveralls.io/repos/github/yar-kik/conjector/badge.svg?branch=master)](https://coveralls.io/github/yar-kik/conjector?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


## What is this
It is a simple library to inject non-sensitive configurations into class variables.
Basically, it's like `BaseSettings` in `pydantic` library but for constants in `json`, `yaml`, `toml` or `ini` formats.
`conjector` can work with different Python types (like `tuple`, `datetime`, `dataclass` and so on) and recursively cast config values to them.

More information about the library and all features you can find in the official [documentation](https://conjector.readthedocs.io/en/latest/).

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
By default, `conjector` work only with the builtin `json` and `ini` deserializers.
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
from conjector import properties


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


## Different environments
Using this library it's easy to manage different environments and corresponding config files.
It could be done like so:

```python
import os
from conjector import properties


@properties(filename=os.getenv("CONFIG_FILENAME", "application.yml"))
class SomeEnvDependingService:
    env_depend_var: str
```
In this case, you can set `CONFIG_FILENAME=application-dev.yml` in env variables, and `conjector` will use that file.


## About contributing
You will make `conjector` better if you open issues or create pull requests with improvements.
