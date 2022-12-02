from typing import List, Optional, Union

import pytest

from app_properties import properties


class BaseClass:
    optional_int_empty: Optional[int]
    optional_int_wrong_value: Optional[int]
    optional_int_presented: Optional[int]
    optional_list_empty: Optional[List[int]]
    optional_list_presented: Optional[List[int]]

    union_float_int_str: Union[float, int, str]
    union_int_float_str: Union[int, float, str]
    union_str_int_float: Union[str, float, int]
    union_dict_list_presented_dict: Union[dict, List[dict]]
    union_dict_list_presented_list: Union[dict, List[dict]]

    list_optional_int_mixed: List[Optional[int]]
    list_union_int_str_mixed: List[Union[int, str]]


@pytest.fixture
def union_class_fixt():
    @properties(filename="types_cast.yml", root="union")
    class UnionClass(BaseClass):
        pass

    return UnionClass


def test_optional_field(union_class_fixt):
    assert union_class_fixt.optional_int_empty is None
    assert union_class_fixt.optional_int_wrong_value is None
    assert union_class_fixt.optional_int_presented == 10
    assert union_class_fixt.optional_list_empty is None
    assert union_class_fixt.optional_list_presented == [12, 14, 16]


def test_union_field(union_class_fixt):
    assert union_class_fixt.union_float_int_str == 10.5
    assert union_class_fixt.union_int_float_str == 10
    assert union_class_fixt.union_str_int_float == "10.5"
    assert union_class_fixt.union_dict_list_presented_dict == {"key": "value"}
    assert union_class_fixt.union_dict_list_presented_list == [
        {"key": "value"}
    ]


def test_mixed_union_field(union_class_fixt):
    assert union_class_fixt.list_optional_int_mixed == [20, None, 40]
    assert union_class_fixt.list_union_int_str_mixed == [50, "str", "str2", 60]


def test_cannot_cast_to_any_type():
    with pytest.raises(ValueError):

        @properties(filename="types_cast.yml", root="union")
        class NotCastUnionClass:
            wrong_union_dict_list: Union[dict, List[dict]]
