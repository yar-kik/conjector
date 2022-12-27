import pytest

from app_properties import properties


class BaseClass:
    list_var: list
    dict_var: dict
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


def test_wrong_type_is_not_supported():
    with pytest.raises(NotImplementedError):

        @properties(filename="file_with_invalid.ext")
        class WrongConfigType(BaseClass):
            ...
