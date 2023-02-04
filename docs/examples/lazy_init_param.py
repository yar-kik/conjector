from typing import List, Optional, Tuple, TypedDict, Union

from dataclasses import dataclass
from datetime import timedelta

from conjector import properties


@dataclass
class TextStyle:
    size: int
    weight: str
    font: str
    color: Union[Tuple[int, int, int], str]


class GreetingDict(TypedDict):
    language: str
    text: str


@properties(lazy_init=True)
@dataclass
class EmailMessageServiceConfig:
    default_text_style: TextStyle
    language_greetings: List[GreetingDict]
    mailing_frequency: Optional[timedelta] = None
    wellcome_message: str = "some_default_message"


email_config = EmailMessageServiceConfig(
    default_text_style=TextStyle(
        size=16, weight="normal", font="Arial", color="black"
    ),
    language_greetings=[GreetingDict(language="english", text="hello")],
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
