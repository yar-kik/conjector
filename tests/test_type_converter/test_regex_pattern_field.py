import pytest
import re
from re import Pattern

from app_properties import properties


@pytest.fixture
def regex_class_fixt(request):
    @properties(filename=request.param, root="regex")
    class RegexClass:
        some_pattern_var: Pattern

    return RegexClass


@pytest.mark.parametrize(
    "regex_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml"),
    indirect=True,
)
def test_regex_pattern_field(regex_class_fixt):
    assert regex_class_fixt.some_pattern_var == re.compile(r"\w+")


@pytest.mark.parametrize(
    "filename", ("types_cast.yml", "types_cast.json", "types_cast.toml")
)
def test_regex_pattern_wrong_value(filename):
    with pytest.raises(ValueError):

        @properties(filename=filename, root="regex")
        class WrongRegexClass:
            wrong_pattern_var: Pattern
