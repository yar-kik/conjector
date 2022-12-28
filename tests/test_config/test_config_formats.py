import contextlib
import importlib
import pytest
import sys

from app_properties import properties


class BaseClass:
    list_var: list
    dict_var: dict
    int_var: int


@contextlib.contextmanager
def mock_import(module_name: str) -> None:
    module = importlib.import_module(module_name)
    sys.modules[module_name] = None
    yield
    sys.modules[module_name] = module


def test_yaml_config_format_ok():
    @properties(filename="application.yml")
    class YamlConfigClass(BaseClass):
        pass

    assert YamlConfigClass.list_var == ["a", "b", "c"]
    assert YamlConfigClass.dict_var == {"key": "value"}
    assert YamlConfigClass.int_var == 12


def test_yaml_config_format_not_found():
    with mock_import("yaml"):
        with pytest.raises(ImportError):

            @properties(filename="application.yml")
            class YamlConfigClass(BaseClass):
                pass


def test_toml_config_format_ok():
    @properties(filename="application.toml")
    class TomlConfigClass(BaseClass):
        pass

    assert TomlConfigClass.list_var == ["a", "b", "c"]
    assert TomlConfigClass.dict_var == {"key": "value"}
    assert TomlConfigClass.int_var == 12


def test_toml_config_format_not_found():
    with mock_import("toml"):
        with pytest.raises(ImportError):

            @properties(filename="application.toml")
            class TomlConfigClass(BaseClass):
                pass


def test_json_config_format_faster_version():
    @properties(filename="application.json")
    class JsonConfigClass(BaseClass):
        pass

    assert JsonConfigClass.list_var == ["a", "b", "c"]
    assert JsonConfigClass.dict_var == {"key": "value"}
    assert JsonConfigClass.int_var == 12


def test_json_config_format_builtin_version():
    with mock_import("ujson"):

        @properties(filename="application.json")
        class JsonConfigClass(BaseClass):
            pass

        assert JsonConfigClass.list_var == ["a", "b", "c"]
        assert JsonConfigClass.dict_var == {"key": "value"}
        assert JsonConfigClass.int_var == 12
