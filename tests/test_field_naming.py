from main import inject_properties


class BaseCase:
    snake_case: str
    camelCase: str
    PascalCase: str


@inject_properties(ignore_case=False)
class CaseSensitive(BaseCase):
    pass


@inject_properties
class CaseInsensitive(BaseCase):
    pass


@inject_properties
class ClassWithHyphen:
    class_var_with_hyphens: str
    class_var_with_underscores: str
    class_var_with_mixed: str


def test_case_sensitive_fields():
    assert CaseSensitive.camelCase == "camelCase"
    assert CaseSensitive.snake_case == "snake_case"
    assert CaseSensitive.PascalCase == "PascalCase"


def test_case_insensitive_fields():
    assert CaseInsensitive.camelCase == "camelcase"
    assert CaseInsensitive.snake_case == "snake_case"
    assert CaseInsensitive.PascalCase == "pascalcase"


def test_properties_with_hyphens():
    assert ClassWithHyphen.class_var_with_hyphens == "class-var-with-hyphens"
    assert ClassWithHyphen.class_var_with_underscores == "class_var_with_underscores"
    assert ClassWithHyphen.class_var_with_mixed == "class_var-with-mixed"
