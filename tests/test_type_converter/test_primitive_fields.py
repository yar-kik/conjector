import pytest

from app_properties import properties


class BaseClass:
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@pytest.fixture
def not_cast_primitive_class_fixt():
    @properties(filename="types_cast.yml", root="primitive", type_cast=False)
    class NotCastPrimitiveClass(BaseClass):
        pass

    return NotCastPrimitiveClass


@pytest.fixture
def cast_primitive_class_fixt():
    @properties(filename="types_cast.yml", root="primitive")
    class CastPrimitiveClass(BaseClass):
        pass

    return CastPrimitiveClass


def test_not_cast_vars(not_cast_primitive_class_fixt):
    assert not_cast_primitive_class_fixt.int_var == "10"
    assert not_cast_primitive_class_fixt.float_var == "10.5"
    assert not_cast_primitive_class_fixt.bool_var == True
    assert not_cast_primitive_class_fixt.none_var == None
    assert not_cast_primitive_class_fixt.str_var == "str"


def test_cast_vars(cast_primitive_class_fixt):
    assert cast_primitive_class_fixt.int_var == 10
    assert cast_primitive_class_fixt.float_var == 10.5
    assert cast_primitive_class_fixt.bool_var == True
    assert cast_primitive_class_fixt.none_var == None
    assert cast_primitive_class_fixt.str_var == "str"
