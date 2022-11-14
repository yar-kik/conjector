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


@pytest.fixture
def json_config_fixt():
    @properties(filename="tests/application.json")
    class JSONConfig(BaseClass):
        pass

    return JSONConfig


@pytest.fixture
def yaml_config_fixt():
    @properties(filename="tests/application.yml")
    class YAMLConfig(BaseClass):
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

        @properties(filename="tests/file_with_invalid.ext")
        class WrongConfigType(BaseClass):
            ...
