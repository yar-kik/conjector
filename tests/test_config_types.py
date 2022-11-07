import pytest

from app_properties import properties


class BaseVar:
    list_var: list
    dict_var: dict
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@pytest.fixture
def json_config_fixt():
    @properties(filename="application.json")
    class JSONConfig(BaseVar):
        pass

    return JSONConfig


@pytest.fixture
def yaml_config_fixt():
    @properties
    class YAMLConfig(BaseVar):
        pass

    return YAMLConfig


def test_config_different_types_equal(json_config_fixt, yaml_config_fixt):
    assert json_config_fixt.bool_var == yaml_config_fixt.bool_var
    assert json_config_fixt.dict_var == yaml_config_fixt.dict_var
    assert json_config_fixt.list_var == yaml_config_fixt.list_var
    assert json_config_fixt.int_var == yaml_config_fixt.int_var
    assert json_config_fixt.float_var == yaml_config_fixt.float_var
    assert json_config_fixt.none_var == yaml_config_fixt.none_var
    assert json_config_fixt.str_var == yaml_config_fixt.str_var


def test_wrong_type_is_not_supported():
    with pytest.raises(NotImplementedError):

        @properties(filename="file_with_invalid.ext")
        class WrongConfigType(BaseVar):
            ...
