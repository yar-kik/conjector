from typing import List, Dict

from main import inject_properties


class BaseVar:
    list_var: List[int]
    dict_var: Dict[str, bool]
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@inject_properties(filename="types_cast.yml")
class NotCastedVar(BaseVar):
    pass


@inject_properties(filename="types_cast.yml", cast=True)
class CastedVar(BaseVar):
    pass


@inject_properties(filename="not_existing.yml")
class DefaultNotCastedVar(BaseVar):
    pass


@inject_properties(filename="not_existing.yml", cast=True)
class DefaultCastedVar(BaseVar):
    pass


def test_not_casted_vars():
    assert NotCastedVar.list_var == ["1", "2", "3"]
    assert NotCastedVar.dict_var == {"key": "false"}
    assert NotCastedVar.int_var == "10"
    assert NotCastedVar.float_var == "10.5"
    assert NotCastedVar.bool_var == True
    assert NotCastedVar.none_var == None
    assert NotCastedVar.str_var == "str"


def test_casted_vars():
    assert CastedVar.list_var == ["1", "2", "3"]
    assert CastedVar.dict_var == {"key": "false"}
    assert CastedVar.int_var == 10
    assert CastedVar.float_var == 10.5
    assert CastedVar.bool_var == True
    assert CastedVar.none_var == None
    assert CastedVar.str_var == "str"


def test_default_not_casted():
    assert DefaultNotCastedVar.list_var is None
    assert DefaultNotCastedVar.dict_var is None
    assert DefaultNotCastedVar.int_var is None
    assert DefaultNotCastedVar.float_var is None
    assert DefaultNotCastedVar.bool_var is None
    assert DefaultNotCastedVar.none_var is None
    assert DefaultNotCastedVar.str_var is None


def test_default_casted():
    assert DefaultCastedVar.list_var is None
    assert DefaultCastedVar.dict_var is None
    assert DefaultCastedVar.int_var == 0
    assert DefaultCastedVar.float_var == 0.0
    assert DefaultCastedVar.bool_var == False
    assert DefaultCastedVar.none_var is None
    assert DefaultCastedVar.str_var == ""
