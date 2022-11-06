import pytest

from main import inject_properties


class BaseVar:
    list_var: list
    dict_var: dict
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@inject_properties(filename="application.json")
class JSONConfig(BaseVar):
    pass


@inject_properties
class YAMLConfig(BaseVar):
    pass


def test_config_different_types_equal():
    assert JSONConfig.bool_var == YAMLConfig.bool_var
    assert JSONConfig.dict_var == YAMLConfig.dict_var
    assert JSONConfig.list_var == YAMLConfig.list_var
    assert JSONConfig.int_var == YAMLConfig.int_var
    assert JSONConfig.float_var == YAMLConfig.float_var
    assert JSONConfig.none_var == YAMLConfig.none_var
    assert JSONConfig.str_var == YAMLConfig.str_var


def test_wrong_type_is_not_supported():
    with pytest.raises(NotImplementedError):
        clss = type("WrongConfigType", (BaseVar,), {})
        inject_properties(clss, filename="file_with_invalid.ext")
