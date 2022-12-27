import pytest
from dataclasses import dataclass

from app_properties import properties


@dataclass
class CustomClass:
    int_var: int
    str_var: str


class BaseClass:
    list_var: list
    set_var: set
    dict_var: dict
    tuple_var: tuple
    dataclass_var: CustomClass


@pytest.fixture
def base_class_fixt(request):
    @properties(filename=request.param, root="base")
    class Base(BaseClass):
        pass

    return Base


@pytest.mark.parametrize(
    "base_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml"),
    indirect=True,
)
def test_field_if_not_empty_in_config(base_class_fixt):
    assert base_class_fixt.dict_var == dict()
    assert base_class_fixt.tuple_var == tuple()
    assert base_class_fixt.set_var == set()
    assert base_class_fixt.list_var == list()
    assert base_class_fixt.dataclass_var == CustomClass(int_var=0, str_var="")
