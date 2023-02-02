from typing import Dict, List

import pytest

from conjector.main import Conjector, properties


@pytest.fixture
def base_fixt():
    class BaseClass:
        list_var: List[str]
        dict_var: Dict[str, str]
        int_var: int
        bool_var: bool

    return BaseClass


@pytest.fixture
def decorator_fixt():
    @properties
    class DecoratorClass:
        list_var: List[str]
        dict_var: Dict[str, str]
        int_var: int
        bool_var: bool

    return DecoratorClass


def test_conjector_same_to_decorator(decorator_fixt, base_fixt):
    config_injector = Conjector()
    injected_class = config_injector.inject_config(base_fixt)
    assert injected_class.int_var == decorator_fixt.int_var
    assert injected_class.list_var == decorator_fixt.list_var
    assert injected_class.dict_var == decorator_fixt.dict_var
    assert injected_class.bool_var == decorator_fixt.bool_var


def test_conjector_affect_on_original_class(base_fixt):
    config_injector = Conjector()
    config_injector.inject_config(base_fixt)
    assert base_fixt.int_var == 10
    assert base_fixt.list_var == ["a", "b", "c"]
    assert base_fixt.dict_var == {"key": "value"}
    assert base_fixt.bool_var
