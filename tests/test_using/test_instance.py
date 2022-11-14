from app_properties import properties


@properties(filename="tests/application.yml")
class BaseClass:
    list_var: list
    dict_var: dict
    int_var: int
    str_var: str

    def __init__(self, str_var: str, int_var: int) -> None:
        self.str_var = str_var
        self.int_var = int_var


def test_class_vars_after_init_will_be_overriden():
    int_var = 20
    str_var = "str_var"
    base_var = BaseClass(str_var, int_var)
    assert base_var.list_var == ["a", "b", "c"]
    assert base_var.dict_var == {"key": "value"}
    assert base_var.int_var == int_var
    assert base_var.str_var == str_var
