# Quickstart
## Installation

To install this library just enter:
```shell
pip install conjector
```
By default, `conjector` work only with the builtin `json` and `ini` deserializers.

To work with `yaml`:
```shell
pip install conjector[yaml]
```
To work with `toml` if you are using Python <= 3.10:
```shell
pip install conjector[toml]
```
And for faster version of json deserializer:
```shell
pip install conjector[json]
```
Also, you can download required extensions like so:
```shell
pip install conjector[yaml,toml]
```
And if you want to download all supported config formats:
```shell
pip install conjector[all]
```

## Using

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
You can also check what other [parameters](parameters.md) the decorator can accept.
