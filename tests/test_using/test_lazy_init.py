import pytest
from dataclasses import dataclass

from conjector import properties


@pytest.fixture
def lazy_init_fixt():
    @properties(root="lazy_init", lazy_init=True)
    @dataclass
    class LazyInitClass:
        init_var: str
        config_var: str
        init_default_var: str = "not_exist_value"
        config_default_var: str = "default_value"

    return LazyInitClass


def test_lazy_init_provided_only_default(lazy_init_fixt):
    instance = lazy_init_fixt(init_var="init_var", config_var="new_value")
    instance.init_props()
    assert instance.init_default_var == "not_exist_value"


def test_lazy_init_provided_only_init(lazy_init_fixt):
    instance = lazy_init_fixt(init_var="init_var", config_var="new_value")
    instance.init_props()
    assert instance.init_var == "init_var"


def test_lazy_init_provided_default_and_config(lazy_init_fixt):
    instance = lazy_init_fixt(init_var="init_var", config_var="new_value")
    instance.init_props()
    assert instance.config_default_var == "another_config_value"


def test_lazy_init_provided_all_and_override_init(lazy_init_fixt):
    instance = lazy_init_fixt(
        init_var="init_var",
        config_var="new_value",
        config_default_var="new_default_value",
    )
    instance.init_props()
    assert instance.config_var == "some_config_value"
    assert instance.config_default_var == "another_config_value"


def test_lazy_init_provided_all_and_keep_init(lazy_init_fixt):
    instance = lazy_init_fixt(
        init_var="init_var",
        config_var="new_value",
        config_default_var="new_default_value",
    )
    instance.init_props(override_init=False)
    assert instance.config_var == "new_value"
    assert instance.config_default_var == "new_default_value"
