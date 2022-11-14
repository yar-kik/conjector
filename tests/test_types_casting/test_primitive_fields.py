import pytest

from app_properties import properties


class BaseClass:
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@pytest.fixture
def not_casted_primitive_class_fixt():
    @properties(filename="tests/types_cast.yml", root="primitive")
    class NotCastedPrimitiveClass(BaseClass):
        pass

    return NotCastedPrimitiveClass


@pytest.fixture
def casted_primitive_class_fixt():
    @properties(
        filename="tests/types_cast.yml", type_cast=True, root="primitive"
    )
    class CastedPrimitiveClass(BaseClass):
        pass

    return CastedPrimitiveClass


def test_not_casted_vars(not_casted_primitive_class_fixt):
    assert not_casted_primitive_class_fixt.int_var == "10"
    assert not_casted_primitive_class_fixt.float_var == "10.5"
    assert not_casted_primitive_class_fixt.bool_var == True
    assert not_casted_primitive_class_fixt.none_var == None
    assert not_casted_primitive_class_fixt.str_var == "str"


def test_casted_vars(casted_primitive_class_fixt):
    assert casted_primitive_class_fixt.int_var == 10
    assert casted_primitive_class_fixt.float_var == 10.5
    assert casted_primitive_class_fixt.bool_var == True
    assert casted_primitive_class_fixt.none_var == None
    assert casted_primitive_class_fixt.str_var == "str"
