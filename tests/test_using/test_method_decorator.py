from typing import Tuple

from conjector import properties
from conjector.entities import Default
from tests.conftest import patch_config


class SomeClass:
    @properties
    def __init__(self, a: int = Default(), b: int = Default()) -> None:
        self.a = a
        self.b = b

    @properties
    def simple_method(
        self, a: int = Default(), b: int = Default()
    ) -> Tuple[int, int]:
        return a, b

    @classmethod
    @properties
    def cls_method(
        cls, a: int = Default(), b: int = Default()
    ) -> Tuple[int, int]:
        return a, b

    @staticmethod
    @properties
    def stat_method(a: int = Default(), b: int = Default()) -> Tuple[int, int]:
        return a, b


@patch_config({"a": 10, "b": 20})
def test_decorator_on_magic_method():
    obj = SomeClass()
    assert obj.a, obj.b == (10, 20)


@patch_config({"a": 10, "b": 20})
def test_decorator_on_classmethod():
    assert SomeClass.cls_method() == (10, 20)


@patch_config({"a": 10, "b": 20})
def test_decorator_on_staticmethod():
    assert SomeClass.stat_method() == (10, 20)


@patch_config({"a": 10, "b": 20})
def test_decorator_on_simple_method():
    obj = SomeClass()
    assert obj.simple_method() == (10, 20)
