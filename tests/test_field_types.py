from main import inject_properties


class BaseVar:
    list_var: list
    dict_var: dict
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


@inject_properties(filename="not_existing.yml")
class NotExistingProps(BaseVar):
    pass


@inject_properties
class ExistingProps(BaseVar):
    pass


@inject_properties
class WithoutParens(BaseVar):
    pass


@inject_properties()
class WithParens(BaseVar):
    pass


def test_class_variables_if_not_default_and_property_not_exists():
    assert NotExistingProps.bool_var is None
    assert NotExistingProps.dict_var is None
    assert NotExistingProps.list_var is None
    assert NotExistingProps.int_var is None
    assert NotExistingProps.float_var is None
    assert NotExistingProps.none_var is None
    assert NotExistingProps.str_var is None


def test_class_variables_if_properties_exist():
    assert ExistingProps.bool_var == True
    assert ExistingProps.dict_var == {"key": "value"}
    assert ExistingProps.list_var == ["a", "b", "c"]
    assert ExistingProps.int_var == 10
    assert ExistingProps.float_var == 10.5
    assert ExistingProps.none_var is None
    assert ExistingProps.str_var == "str"


def test_decorator_with_and_without_parens_are_same():
    assert WithParens.bool_var == WithoutParens.bool_var
    assert WithParens.dict_var == WithoutParens.dict_var
    assert WithParens.list_var == WithoutParens.list_var
    assert WithParens.int_var == WithoutParens.int_var
    assert WithParens.float_var == WithoutParens.float_var
    assert WithParens.none_var == WithoutParens.none_var
    assert WithParens.str_var == WithoutParens.str_var
