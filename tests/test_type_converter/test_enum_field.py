import pytest
from enum import Enum, IntEnum

from app_properties import properties


class SimpleEnum(Enum):
    GREEN = "GREEN"
    RED = "READ"


class CustomIntEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3


@pytest.fixture
def enum_class_fixt():
    @properties(filename="types_cast.yml", root="enum")
    class EnumClass:
        simple_enum_var: SimpleEnum
        int_enum_var: CustomIntEnum

    return EnumClass


def test_enum_field(enum_class_fixt):
    assert enum_class_fixt.simple_enum_var == SimpleEnum.GREEN

    assert enum_class_fixt.int_enum_var == CustomIntEnum.THREE
    assert enum_class_fixt.int_enum_var == 3


def test_invalid_enum_field(enum_class_fixt):
    with pytest.raises(ValueError):

        @properties(filename="types_cast.yml", root="enum")
        class InvalidFieldClass:
            invalid_enum_var: SimpleEnum

    with pytest.raises(ValueError):

        @properties(filename="types_cast.yml", root="enum")
        class MissingFieldClass:
            missing_enum_var: SimpleEnum
