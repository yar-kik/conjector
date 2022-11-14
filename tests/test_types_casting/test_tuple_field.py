from typing import NamedTuple, Tuple

import pytest

from app_properties import properties

CustomTuple = NamedTuple("CustomTuple", [("int_var", int), ("str_var", str)])


class BaseClass:
    int_with_ellipsis_tuple_var: Tuple[int, ...]
    int_str_float_tuple_var: Tuple[int, str, float]
    single_int_tuple_var: Tuple[int]
    unspecified_tuple_var: tuple
    keyword_named_tuple_var: CustomTuple
    position_named_tuple_var: CustomTuple


@pytest.fixture
def tuple_class_fixt():
    @properties(filename="tests/types_cast.yml", type_cast=True, root="tuple")
    class TupleClass(BaseClass):
        pass

    return TupleClass


def test_field_with_tuple(tuple_class_fixt):
    assert tuple_class_fixt.int_with_ellipsis_tuple_var == (10, 15)
    assert tuple_class_fixt.keyword_named_tuple_var == CustomTuple(
        int_var=20, str_var="str2"
    )
    assert tuple_class_fixt.position_named_tuple_var == CustomTuple(
        int_var=30, str_var="str3"
    )
    assert tuple_class_fixt.single_int_tuple_var == (40,)
    assert tuple_class_fixt.int_str_float_tuple_var == (50, "60", 70.5)
    assert tuple_class_fixt.unspecified_tuple_var == ("12", "14")


def test_field_with_invalid_tuple():
    with pytest.raises(ValueError):

        @properties(
            filename="tests/types_cast.yml", type_cast=True, root="tuple"
        )
        class InvalidTupleClass:
            wrong_tuple_var: tuple

    with pytest.raises(ValueError):

        @properties(
            filename="tests/types_cast.yml", type_cast=True, root="tuple"
        )
        class InvalidTupleClass:
            wrong_tuple_var: CustomTuple
