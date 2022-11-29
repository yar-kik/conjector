from typing import Any, Dict, TypedDict

import pytest

from app_properties import properties

CustomDict = TypedDict("CustomDict", {"int_var": int, "str_var": str})


class BaseClass:
    simple_dict_var: Dict[str, Any]
    typed_dict_var: CustomDict


@pytest.fixture
def dict_class_fixt():
    @properties(filename="types_cast.yml", root="dict")
    class DictClass(BaseClass):
        pass

    return DictClass


def test_field_with_dict(dict_class_fixt):
    assert dict_class_fixt.simple_dict_var == {
        "int_var": 10,
        "str_var": "str1",
    }
    assert dict_class_fixt.typed_dict_var == CustomDict(
        int_var=20, str_var="str2"
    )


def test_field_with_invalid_dict():
    with pytest.raises(ValueError):

        @properties(filename="types_cast.yml", root="dict")
        class InvalidDictClass:
            wrong_dict_var: dict
