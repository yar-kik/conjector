from typing import Any, Dict, TypedDict

import pytest

from conjector import properties

CustomDict = TypedDict("CustomDict", {"int_var": int, "str_var": str})


class BaseClass:
    simple_dict_var: Dict[str, Any]
    typed_dict_var: CustomDict


@pytest.fixture
def dict_class_fixt(request):
    @properties(filename=request.param, root="dict")
    class DictClass(BaseClass):
        pass

    return DictClass


@pytest.mark.parametrize(
    "dict_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_field_with_dict(dict_class_fixt):
    assert dict_class_fixt.simple_dict_var in (
        {"int_var": 10, "str_var": "str1"},
        {"int_var": "10", "str_var": "str1"},
    )
    assert dict_class_fixt.typed_dict_var == CustomDict(
        int_var=20, str_var="str2"
    )


@pytest.mark.parametrize(
    "filename", ("types_cast.yml", "types_cast.json", "types_cast.toml")
)
def test_field_with_invalid_dict(filename):
    with pytest.raises(ValueError):

        @properties(filename=filename, root="dict")
        class InvalidDictClass:
            wrong_dict_var: dict
