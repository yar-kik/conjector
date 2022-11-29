from typing import List

import pytest
from dataclasses import dataclass, field

from app_properties import properties


@dataclass
class TestClass:
    int_var: int
    list_var: List[str]


@dataclass
class DataclassFieldClass:
    init_false_var: str = field(init=False, compare=False)
    default_var: int = field(default=12)
    default_factory_var: List[int] = field(default_factory=lambda: [15])


@pytest.fixture
def class_with_dataclasses_fixt():
    @properties(filename="types_cast.yml", root="dataclass")
    class MainClass:
        dataclass_var: TestClass
        dataclass_field_class: DataclassFieldClass

    return MainClass


def test_field_is_dataclass(class_with_dataclasses_fixt):
    field_dataclass = DataclassFieldClass(
        default_var=42, default_factory_var=[16, 18]
    )
    assert class_with_dataclasses_fixt.dataclass_var == TestClass(
        int_var=10, list_var=["a", "b", "c"]
    )
    assert class_with_dataclasses_fixt.dataclass_field_class == field_dataclass
    assert not hasattr(
        class_with_dataclasses_fixt.dataclass_field_class, "init_false_var"
    )