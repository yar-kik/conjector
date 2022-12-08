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


@pytest.fixture
def fields_not_presented_fixt():
    @properties(filename="types_cast.yml", root="primitive")
    class DefaultFieldClass:
        default_int_var: int
        default_float_var: float
        default_str_var: str
        default_bool_var: bool
        default_none_var: None

    return DefaultFieldClass


def test_not_cast_vars(not_cast_primitive_class_fixt):
    assert not_cast_primitive_class_fixt.int_var == "10"
    assert not_cast_primitive_class_fixt.float_var == "10.5"
    assert not_cast_primitive_class_fixt.bool_var == True
    assert not_cast_primitive_class_fixt.none_var is None
    assert not_cast_primitive_class_fixt.str_var == "str"


def test_cast_vars(cast_primitive_class_fixt):
    assert cast_primitive_class_fixt.int_var == 10
    assert cast_primitive_class_fixt.float_var == 10.5
    assert cast_primitive_class_fixt.bool_var == True
    assert cast_primitive_class_fixt.none_var is None
    assert cast_primitive_class_fixt.str_var == "str"


def test_default_fields(fields_not_presented_fixt):
    assert fields_not_presented_fixt.default_none_var is None
    assert fields_not_presented_fixt.default_str_var == ""
    assert fields_not_presented_fixt.default_bool_var == False
    assert fields_not_presented_fixt.default_int_var == 0
    assert fields_not_presented_fixt.default_float_var == 0.0


def test_wrong_type_casting():
    with pytest.raises(ValueError):

        @properties(filename="types_cast.yml", root="primitive")
        class WrongIntClass:
            wrong_int_var: int

    with pytest.raises(ValueError):

        @properties(filename="types_cast.yml", root="primitive")
        class WrongFloatClass:
            wrong_float_var: float
