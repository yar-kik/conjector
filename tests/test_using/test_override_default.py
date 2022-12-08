from app_properties import properties


class DefaultVar:
    list_var: list = ["x", "y"]
    dict_var: dict = {"k": "v"}
    int_var: int = 5
    float_var: float = 3.4
    bool_var: bool = False
    none_var: None = None
    str_var: str = "some var"


@properties(filename="application.yml", override_default=True)
class OverrideDefault(DefaultVar):
    pass


@properties(filename="application.yml")
class AllowDefault(DefaultVar):
    pass


def test_allow_default_vars():
    assert AllowDefault.bool_var == False
    assert AllowDefault.dict_var == {"k": "v"}
    assert AllowDefault.list_var == ["x", "y"]
    assert AllowDefault.int_var == 5
    assert AllowDefault.float_var == 3.4
    assert AllowDefault.none_var is None
    assert AllowDefault.str_var == "some var"


def test_override_default_vars():
    assert OverrideDefault.bool_var == True
    assert OverrideDefault.dict_var == {"key": "value"}
    assert OverrideDefault.list_var == ["a", "b", "c"]
    assert OverrideDefault.int_var == 10
    assert OverrideDefault.float_var == 10.5
    assert OverrideDefault.none_var is None
    assert OverrideDefault.str_var == "str"
