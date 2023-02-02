import pytest
from enum import Enum, IntEnum

from conjector import properties


class SimpleEnum(Enum):
    GREEN = "GREEN"
    RED = "READ"


class CustomIntEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3


@pytest.fixture
def enum_class_fixt(request):
    @properties(filename=request.param, root="enum")
    class EnumClass:
        simple_enum_var: SimpleEnum
        int_enum_var: CustomIntEnum

    return EnumClass


@pytest.mark.parametrize(
    "enum_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_enum_field(enum_class_fixt):
    assert enum_class_fixt.simple_enum_var == SimpleEnum.GREEN

    assert enum_class_fixt.int_enum_var == CustomIntEnum.THREE
    assert enum_class_fixt.int_enum_var == 3


@pytest.mark.parametrize(
    "filename",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
)
def test_invalid_enum_field(filename):
    with pytest.raises(ValueError):

        @properties(filename=filename, root="enum")
        class InvalidFieldClass:
            invalid_enum_var: SimpleEnum

    with pytest.raises(ValueError):

        @properties(filename=filename, root="enum")
        class MissingFieldClass:
            missing_enum_var: SimpleEnum
