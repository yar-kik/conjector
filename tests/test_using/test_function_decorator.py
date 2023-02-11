from typing import Any, Tuple

from conjector import properties
from conjector.entities import Default
from tests.conftest import patch_config


@patch_config({"a": "20", "b": "2"})
def test_marked_default_equals_config_value_if_config():
    @properties
    def func(a: int = Default(10), b: int = Default()) -> Tuple[int, int]:
        return a, b

    assert func() == (20, 2)


@patch_config({"a": "20", "b": "2"})
def test_marked_default_equals_uncast_config_value_if_no_type_hint():
    @properties
    def func(a=Default(10), b=Default()) -> Tuple[Any, Any]:
        return a, b

    assert func() == ("20", "2")


@patch_config({})
def test_marked_default_if_no_type_hint_and_config():
    @properties
    def func(a=Default(10), b=Default()) -> Tuple[Any, Any]:
        return a, b

    assert func() == (10, None)


@patch_config({})
def test_marked_default_if_no_config():
    @properties
    def func(a: int = Default(10), b: int = Default()) -> Tuple[int, int]:
        return a, b

    assert func() == (10, 0)


@patch_config({"a": "10", "b": "20"})
def test_decorator_will_not_override_required_args_and_normal_default():
    @properties
    def func(a: int, b: int = 20) -> Tuple[int, int]:
        return a, b

    assert func(10) == (10, 20)


@patch_config({"a": "2", "b": "20"})
def test_function_with_args_and_kwargs():
    @properties
    def func(a: int, b: int = Default(10), *args: int, **kwargs: int) -> tuple:
        return a, b, args, kwargs

    assert func(1, 10, 100, c=1000) == (1, 10, (100,), {"c": 1000})


@patch_config({"a": "2", "b": "20"})
def test_positional_only_func():
    @properties
    def func(a: int, b: int = Default(10), /) -> Tuple[int, int]:
        return a, b

    assert func(1) == (1, 20)


@patch_config({"a": "2", "b": "20"})
def test_keywords_only_func():
    @properties
    def func(*, a: int, b: int = Default(10)) -> Tuple[int, int]:
        return a, b

    assert func(a=1) == (1, 20)


@patch_config({"a": 100, "b": 200})
def test_marked_default_acts_like_normal_default():
    @properties
    def func(a: int = Default(10), b: int = Default()) -> Tuple[int, int]:
        return a, b

    assert func(1, 2) == (1, 2)
