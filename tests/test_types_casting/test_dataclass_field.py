from typing import List

import pytest
from dataclasses import dataclass, field

from app_properties import properties


@dataclass
class TestClass:
    int_var: int
    list_var: List[str]


@dataclass
class NestedClass:
    int_var: int
    dataclass_var: TestClass


@dataclass
class DataclassFieldClass:
    init_false_var: str = field(init=False, compare=False)
    default_var: int = field(default=12)
    default_factory_var: List[int] = field(default_factory=lambda: [15])


@pytest.fixture
def class_with_dataclasses_fixt():
    @properties(filename="tests/dataclasses.yml", type_cast=True)
    class MainClass:
        dataclass_var: TestClass
        list_dataclass_var: List[TestClass]
        nested_class: NestedClass
        dataclass_field_class: DataclassFieldClass

    return MainClass


def test_field_is_dataclass(class_with_dataclasses_fixt):
    assert class_with_dataclasses_fixt.dataclass_var == TestClass(
        int_var=10, list_var=["a", "b", "c"]
    )


def test_field_is_dataclass_list(class_with_dataclasses_fixt):
    assert class_with_dataclasses_fixt.list_dataclass_var == [
        TestClass(int_var=20, list_var=["1", "2", "3"]),
        TestClass(int_var=30, list_var=["4", "5", "6"]),
    ]


def test_field_is_nested_dataclasses(class_with_dataclasses_fixt):
    assert class_with_dataclasses_fixt.nested_class == NestedClass(
        int_var=40,
        dataclass_var=TestClass(int_var=50, list_var=["x", "y", "z"]),
    )


def test_field_is_dataclass_with_custom_field(class_with_dataclasses_fixt):
    field_dataclass = DataclassFieldClass(
        default_var=42, default_factory_var=[16, 18]
    )
    assert class_with_dataclasses_fixt.dataclass_field_class == field_dataclass
    assert not hasattr(
        class_with_dataclasses_fixt.dataclass_field_class, "init_false_var"
    )
