import pytest

from conjector import properties


class BaseClass:
    list_var: list
    dict_var: dict
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@pytest.fixture
def without_parens_fixt():
    @properties
    class WithoutParens(BaseClass):
        pass

    return WithoutParens


@pytest.fixture
def with_parens_fixt():
    @properties()
    class WithParens(BaseClass):
        pass

    return WithParens


def test_decorator_with_and_without_parens_are_same(
    with_parens_fixt, without_parens_fixt
):
    assert with_parens_fixt.bool_var == without_parens_fixt.bool_var
    assert with_parens_fixt.dict_var == without_parens_fixt.dict_var
    assert with_parens_fixt.list_var == without_parens_fixt.list_var
    assert with_parens_fixt.int_var == without_parens_fixt.int_var
    assert with_parens_fixt.float_var == without_parens_fixt.float_var
    assert with_parens_fixt.none_var == without_parens_fixt.none_var
    assert with_parens_fixt.str_var == without_parens_fixt.str_var
