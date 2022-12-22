import pytest
import re
from re import Pattern

from app_properties import properties


@pytest.fixture
def regex_class_fixt():
    @properties(filename="types_cast.yml", root="regex")
    class RegexClass:
        some_pattern_var: Pattern

    return RegexClass


def test_regex_pattern_field(regex_class_fixt):
    assert regex_class_fixt.some_pattern_var == re.compile(r"\w+")


def test_regex_pattern_wrong_value():
    with pytest.raises(ValueError):

        @properties(filename="types_cast.yml", root="regex")
        class WrongRegexClass:
            wrong_pattern_var: Pattern
