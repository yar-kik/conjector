from typing import Dict, List, Set, Tuple

import pytest

from app_properties import properties


class BaseClass:
    list_var: List[int]
    dict_var: Dict[str, bool]
    tuple_var: Tuple[float, float]
    set_var: Set[str]

    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@pytest.fixture
def not_existing_config_fixt():
    @properties(filename="tests/not_existing.yml")
    class NotExistingProps(BaseClass):
        pass

    return NotExistingProps


@pytest.fixture
def default_casted_var_fixt():
    @properties(filename="tests/not_existing.yml", type_cast=True)
    class DefaultCastedVar(BaseClass):
        pass

    return DefaultCastedVar


def test_default_not_casted(not_existing_config_fixt):
    assert not_existing_config_fixt.list_var is None
    assert not_existing_config_fixt.dict_var is None
    assert not_existing_config_fixt.tuple_var is None
    assert not_existing_config_fixt.set_var is None

    assert not_existing_config_fixt.int_var is None
    assert not_existing_config_fixt.float_var is None
    assert not_existing_config_fixt.bool_var is None
    assert not_existing_config_fixt.none_var is None
    assert not_existing_config_fixt.str_var is None


def test_default_casted(default_casted_var_fixt):
    assert default_casted_var_fixt.list_var == []
    assert default_casted_var_fixt.dict_var == {}
    assert default_casted_var_fixt.tuple_var == ()
    assert default_casted_var_fixt.set_var == set()

    assert default_casted_var_fixt.int_var == 0
    assert default_casted_var_fixt.float_var == 0.0
    assert default_casted_var_fixt.bool_var == False
    assert default_casted_var_fixt.none_var is None
    assert default_casted_var_fixt.str_var == ""
