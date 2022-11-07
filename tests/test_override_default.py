from app_properties import properties


class DefaultVar:
    list_var: list = []
    dict_var: dict = {}
    int_var: int = 0
    float_var: float = 0.0
    bool_var: bool = False
    none_var: None = None
    str_var: str = ""


@properties(override_default=True)
class OverrideDefault(DefaultVar):
    pass


@properties
class AllowDefault(DefaultVar):
    pass


def test_allow_default_vars():
    assert AllowDefault.bool_var == False
    assert AllowDefault.dict_var == {}
    assert AllowDefault.list_var == []
    assert AllowDefault.int_var == 0
    assert AllowDefault.float_var == 0.0
    assert AllowDefault.none_var is None
    assert AllowDefault.str_var == ""


def test_override_default_vars():
    assert OverrideDefault.bool_var == True
    assert OverrideDefault.dict_var == {"key": "value"}
    assert OverrideDefault.list_var == ["a", "b", "c"]
    assert OverrideDefault.int_var == 10
    assert OverrideDefault.float_var == 10.5
    assert OverrideDefault.none_var is None
    assert OverrideDefault.str_var == "str"
