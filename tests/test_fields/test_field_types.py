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
def not_existing_config_fixt():
    @properties(filename="not_existing.yml")
    class NotExistingProps(BaseVar):
        pass

    return NotExistingProps


@pytest.fixture
def existing_config_fixt():
    @properties(filename="tests/application.yml")
    class ExistingProps(BaseVar):
        pass

    return ExistingProps


@pytest.fixture
def without_parens_fixt():
    @properties
    class WithoutParens(BaseVar):
        pass

    return WithoutParens


@pytest.fixture
def with_parens_fixt():
    @properties()
    class WithParens(BaseVar):
        pass

    return WithParens


def test_class_variables_if_not_default_and_property_not_exists(
    not_existing_config_fixt,
):
    assert not_existing_config_fixt.bool_var is None
    assert not_existing_config_fixt.dict_var is None
    assert not_existing_config_fixt.list_var is None
    assert not_existing_config_fixt.int_var is None
    assert not_existing_config_fixt.float_var is None
    assert not_existing_config_fixt.none_var is None
    assert not_existing_config_fixt.str_var is None


def test_class_variables_if_properties_exist(existing_config_fixt):
    assert existing_config_fixt.bool_var == True
    assert existing_config_fixt.dict_var == {"key": "value"}
    assert existing_config_fixt.list_var == ["a", "b", "c"]
    assert existing_config_fixt.int_var == 10
    assert existing_config_fixt.float_var == 10.5
    assert existing_config_fixt.none_var is None
    assert existing_config_fixt.str_var == "str"


def test_decorator_with_and_without_parens_are_same(
    with_parens_fixt, without_parens_fixt
):
    assert with_parens_fixt.bool_var == without_parens_fixt.bool_var
    assert with_parens_fixt.dict_var == without_parens_fixt.dict_var
    assert with_parens_fixt.list_var == without_parens_fixt.list_var
    assert with_parens_fixt.int_var == without_parens_fixt.int_var
    assert with_parens_fixt.float_var == without_parens_fixt.float_var
    assert with_parens_fixt.none_var == without_parens_fixt.none_var
    assert with_parens_fixt.str_var == without_parens_fixt.str_var
