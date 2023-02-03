import pytest

from conjector import properties


class BaseCase:
    snake_case: str
    camelCase: str
    PascalCase: str


@pytest.fixture
def case_sensitive_fixt():
    @properties(filename="application.yml")
    class CaseSensitive(BaseCase):
        pass

    return CaseSensitive


@pytest.fixture
def case_insensitive_fixt():
    @properties(filename="application.yml")
    class CaseInsensitive(BaseCase):
        pass

    return CaseInsensitive


@pytest.fixture
def class_var_with_hyphen_fixt():
    @properties(filename="application.yml")
    class ClassWithHyphen:
        class_var_with_hyphens: str
        class_var_with_underscores: str
        class_var_with_mixed: str

    return ClassWithHyphen


def test_case_sensitive_fields(case_sensitive_fixt):
    assert case_sensitive_fixt.camelCase == "camelCase"
    assert case_sensitive_fixt.snake_case == "snake_case"
    assert case_sensitive_fixt.PascalCase == "PascalCase"


def test_properties_with_hyphens(class_var_with_hyphen_fixt):
    assert (
        class_var_with_hyphen_fixt.class_var_with_hyphens
        == "class-var-with-hyphens"
    )
    assert (
        class_var_with_hyphen_fixt.class_var_with_underscores
        == "class_var_with_underscores"
    )
    assert (
        class_var_with_hyphen_fixt.class_var_with_mixed
        == "class_var-with-mixed"
    )
