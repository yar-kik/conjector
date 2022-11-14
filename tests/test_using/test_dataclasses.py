import pytest
from dataclasses import dataclass

from app_properties import properties


@pytest.fixture
def dataclass_fixt():
    @properties(filename="tests/application.yml")
    @dataclass(init=False)
    class BaseClass:
        list_var: list
        dict_var: dict
        int_var: int
        str_var: str

    return BaseClass


def test_dataclass_before_init(dataclass_fixt):
    assert dataclass_fixt.list_var == ["a", "b", "c"]
    assert dataclass_fixt.dict_var == {"key": "value"}
    assert dataclass_fixt.int_var == 10
    assert dataclass_fixt.str_var == "str"


def test_dataclass_after_init(dataclass_fixt):
    dto = dataclass_fixt()
    assert dto.list_var == ["a", "b", "c"]
    assert dto.dict_var == {"key": "value"}
    assert dto.int_var == 10
    assert dto.str_var == "str"
