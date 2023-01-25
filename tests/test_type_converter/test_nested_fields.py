from typing import List, NamedTuple, Set, Tuple, TypedDict

import pytest
from dataclasses import dataclass

from app_properties import properties

ListWithInt = List[int]
CustomTuple = NamedTuple(
    "CustomTuple", [("int_var", int), ("list_with_int", ListWithInt)]
)
CustomDict = TypedDict("CustomDict", {"namedtuple": CustomTuple})


@dataclass
class InnerCustomClass:
    set_with_str: Set[str]
    tuple_with_float: Tuple[float, ...]


@dataclass
class CustomClass:
    list_with_int: ListWithInt
    typeddict: CustomDict
    namedtuple: CustomTuple
    inner_class: InnerCustomClass


class BaseClass:
    list_with_int: ListWithInt
    typeddict_with_namedtuple: CustomDict
    dataclass_with_nested: CustomClass


@pytest.fixture
def nested_class_fixt(request):
    @properties(filename=request.param, root="nested")
    class NestedClass(BaseClass):
        pass

    return NestedClass


@pytest.mark.parametrize(
    "nested_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_fields_with_nested_types(nested_class_fixt):
    assert nested_class_fixt.list_with_int == [1, 2, 3]
    assert nested_class_fixt.typeddict_with_namedtuple == CustomDict(
        namedtuple=CustomTuple(int_var=10, list_with_int=[12, 14, 16])
    )
    assert nested_class_fixt.dataclass_with_nested == CustomClass(
        list_with_int=[4, 5, 6],
        typeddict=CustomDict(
            namedtuple=CustomTuple(int_var=20, list_with_int=[22, 24, 26])
        ),
        namedtuple=CustomTuple(int_var=30, list_with_int=[30, 33, 36]),
        inner_class=InnerCustomClass(
            set_with_str={"7", "8", "9"}, tuple_with_float=(10.5, 12.0, 13.5)
        ),
    )
