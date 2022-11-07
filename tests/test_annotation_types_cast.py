from typing import Dict, List

import pytest

from app_properties import properties


class BaseVar:
    list_var: List[int]
    dict_var: Dict[str, bool]
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@pytest.fixture
def not_casted_var_fixt():
    @properties(filename="types_cast.yml")
    class NotCastedVar(BaseVar):
        pass

    return NotCastedVar


@pytest.fixture
def casted_var_fixt():
    @properties(filename="types_cast.yml", type_cast=True)
    class CastedVar(BaseVar):
        pass

    return CastedVar


@pytest.fixture
def default_not_casted_var_fixt():
    @properties(filename="not_existing.yml")
    class DefaultNotCastedVar(BaseVar):
        pass

    return DefaultNotCastedVar


@pytest.fixture
def default_casted_var_fixt():
    @properties(filename="not_existing.yml", type_cast=True)
    class DefaultCastedVar(BaseVar):
        pass

    return DefaultCastedVar


def test_not_casted_vars(not_casted_var_fixt):
    assert not_casted_var_fixt.list_var == ["1", "2", "3"]
    assert not_casted_var_fixt.dict_var == {"key": "false"}
    assert not_casted_var_fixt.int_var == "10"
    assert not_casted_var_fixt.float_var == "10.5"
    assert not_casted_var_fixt.bool_var == True
    assert not_casted_var_fixt.none_var == None
    assert not_casted_var_fixt.str_var == "str"


def test_casted_vars(casted_var_fixt):
    assert casted_var_fixt.list_var == ["1", "2", "3"]
    assert casted_var_fixt.dict_var == {"key": "false"}
    assert casted_var_fixt.int_var == 10
    assert casted_var_fixt.float_var == 10.5
    assert casted_var_fixt.bool_var == True
    assert casted_var_fixt.none_var == None
    assert casted_var_fixt.str_var == "str"


def test_default_not_casted(default_not_casted_var_fixt):
    assert default_not_casted_var_fixt.list_var is None
    assert default_not_casted_var_fixt.dict_var is None
    assert default_not_casted_var_fixt.int_var is None
    assert default_not_casted_var_fixt.float_var is None
    assert default_not_casted_var_fixt.bool_var is None
    assert default_not_casted_var_fixt.none_var is None
    assert default_not_casted_var_fixt.str_var is None


def test_default_casted(default_casted_var_fixt):
    assert default_casted_var_fixt.list_var == []
    assert default_casted_var_fixt.dict_var == {}
    assert default_casted_var_fixt.int_var == 0
    assert default_casted_var_fixt.float_var == 0.0
    assert default_casted_var_fixt.bool_var == False
    assert default_casted_var_fixt.none_var is None
    assert default_casted_var_fixt.str_var == ""
