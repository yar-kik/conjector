from main import inject_properties


class BaseVar:
    list_var: list
    dict_var: dict
    int_var: int
    float_var: float
    bool_var: bool
    none_var: None
    str_var: str


class DefaultVar:
    list_var: list = []
    dict_var: dict = {}
    int_var: int = 0
    float_var: float = 0.0
    bool_var: bool = False
    none_var: None = None
    str_var: str = ""


@inject_properties(filename="not_existing.yml")
class DefaultVarNotExistingProps(DefaultVar):
    pass


@inject_properties(filename="not_existing.yml")
class BaseVarNotExistingProps(BaseVar):
    pass


@inject_properties
class BaseVarExistingProps(BaseVar):
    pass


@inject_properties
class DefaultVarExistingProps(DefaultVar):
    pass


@inject_properties
class WithoutParens(BaseVar):
    pass


@inject_properties()
class WithParens(BaseVar):
    pass


def test_class_variables_if_not_default_and_property_not_exists():
    assert BaseVarNotExistingProps.bool_var is None
    assert BaseVarNotExistingProps.dict_var is None
    assert BaseVarNotExistingProps.list_var is None
    assert BaseVarNotExistingProps.int_var is None
    assert BaseVarNotExistingProps.float_var is None
    assert BaseVarNotExistingProps.none_var is None
    assert BaseVarNotExistingProps.str_var is None


def test_class_variables_if_default_and_property_not_exists():
    assert DefaultVarNotExistingProps.bool_var == False
    assert DefaultVarNotExistingProps.dict_var == {}
    assert DefaultVarNotExistingProps.list_var == []
    assert DefaultVarNotExistingProps.int_var == 0
    assert DefaultVarNotExistingProps.float_var == 0.0
    assert DefaultVarNotExistingProps.none_var is None
    assert DefaultVarNotExistingProps.str_var == ""


def test_class_variables_if_default_and_property_exists():
    assert DefaultVarExistingProps.bool_var == False
    assert DefaultVarExistingProps.dict_var == {}
    assert DefaultVarExistingProps.list_var == []
    assert DefaultVarExistingProps.int_var == 0
    assert DefaultVarExistingProps.float_var == 0.0
    assert DefaultVarExistingProps.none_var is None
    assert DefaultVarExistingProps.str_var == ""


def test_class_variables_if_properties_exist():
    assert BaseVarExistingProps.bool_var == True
    assert BaseVarExistingProps.dict_var == {"key": "value"}
    assert BaseVarExistingProps.list_var == ["a", "b", "c"]
    assert BaseVarExistingProps.int_var == 10
    assert BaseVarExistingProps.float_var == 10.5
    assert BaseVarExistingProps.none_var is None
    assert BaseVarExistingProps.str_var == "str"


def test_decorator_with_and_without_parens_are_same():
    assert WithParens.bool_var == WithoutParens.bool_var
    assert WithParens.dict_var == WithoutParens.dict_var
    assert WithParens.list_var == WithoutParens.list_var
    assert WithParens.int_var == WithoutParens.int_var
    assert WithParens.float_var == WithoutParens.float_var
    assert WithParens.none_var == WithoutParens.none_var
    assert WithParens.str_var == WithoutParens.str_var
