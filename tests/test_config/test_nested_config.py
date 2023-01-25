import pytest

from app_properties import properties


class Base:
    str_var: str
    int_var: int


@pytest.fixture
def zero_root_fixt(request):
    @properties(filename=request.param)
    class ZeroRoot(Base):
        pass

    return ZeroRoot


@pytest.fixture
def first_level_fixt(request):
    @properties(filename=request.param, root="first")
    class FirstLevelRoot(Base):
        pass

    return FirstLevelRoot


@pytest.fixture
def second_level_fixt(request):
    @properties(filename=request.param, root="second.first")
    class SecondLevelRoot(Base):
        pass

    return SecondLevelRoot


@pytest.fixture
def third_level_fixt(request):
    @properties(filename=request.param, root="third.second.first")
    class ThirdLevelRoot(Base):
        pass

    return ThirdLevelRoot


@pytest.mark.parametrize(
    "zero_root_fixt",
    (
        "application.yml",
        "application.json",
        "application.toml",
        "application.ini",
    ),
    indirect=True,
)
def test_default_root(zero_root_fixt):
    assert zero_root_fixt.str_var == "root"
    assert zero_root_fixt.int_var == 5


@pytest.mark.parametrize(
    "first_level_fixt",
    (
        "application.yml",
        "application.json",
        "application.toml",
        "application.ini",
    ),
    indirect=True,
)
def test_first_level_root(first_level_fixt):
    assert first_level_fixt.str_var == "first"
    assert first_level_fixt.int_var == 10


@pytest.mark.parametrize(
    "second_level_fixt",
    (
        "application.yml",
        "application.json",
        "application.toml",
        "application.ini",
    ),
    indirect=True,
)
def test_second_level_root(second_level_fixt):
    assert second_level_fixt.str_var == "second"
    assert second_level_fixt.int_var == 20


@pytest.mark.parametrize(
    "third_level_fixt",
    (
        "application.yml",
        "application.json",
        "application.toml",
        "application.ini",
    ),
    indirect=True,
)
def test_third_level_root(third_level_fixt):
    assert third_level_fixt.str_var == "third"
    assert third_level_fixt.int_var == 30
