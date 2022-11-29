from app_properties import properties


class Base:
    str_var: str
    int_var: int


@properties(filename="nested_conf.yml")
class ZeroRoot(Base):
    pass


@properties(filename="nested_conf.yml", root="first")
class FirstLevelRoot(Base):
    pass


@properties(filename="nested_conf.yml", root="second.first")
class SecondLevelRoot(Base):
    pass


@properties(filename="nested_conf.yml", root="third.second.first")
class ThirdLevelRoot(Base):
    pass


def test_default_root():
    assert ZeroRoot.str_var == "root"
    assert ZeroRoot.int_var == 0


def test_first_level_root():
    assert FirstLevelRoot.str_var == "first"
    assert FirstLevelRoot.int_var == 10


def test_second_level_root():
    assert SecondLevelRoot.str_var == "second"
    assert SecondLevelRoot.int_var == 20


def test_third_level_root():
    assert ThirdLevelRoot.str_var == "third"
    assert ThirdLevelRoot.int_var == 30
