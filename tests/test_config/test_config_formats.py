import pytest
import sys
from unittest.mock import patch

from conjector import properties
from conjector.config_handler import ConfigHandler


class BaseClass:
    list_var: list
    dict_var: dict
    int_var: int


def test_yaml_config_format_with_cloader():
    @properties(filename="application.yml")
    class YamlConfigClass(BaseClass):
        pass

    assert YamlConfigClass.list_var == ["a", "b", "c"]
    assert YamlConfigClass.dict_var == {"key": "value"}
    assert YamlConfigClass.int_var == 5


def test_yaml_config_format_with_pyloader():
    with patch.dict(sys.modules["yaml"].__dict__) as patched_yaml:
        del patched_yaml["CSafeLoader"]

        @properties(filename="application.yml")
        class YamlConfigClass(BaseClass):
            pass

        assert YamlConfigClass.list_var == ["a", "b", "c"]
        assert YamlConfigClass.dict_var == {"key": "value"}
        assert YamlConfigClass.int_var == 5


def test_yaml_config_format_pyyaml_not_found():
    with patch("conjector.config_handler.yaml", None):
        with pytest.raises(ImportError):

            @properties(filename="application.yml")
            class YamlConfigClass(BaseClass):
                pass


@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="'tomllib' is available only for python with version >= 3.11",
)
def test_toml_config_format_tomllib_ok():
    @properties(filename="application.toml")
    class TomlConfigClass(BaseClass):
        pass

    assert TomlConfigClass.list_var == ["a", "b", "c"]
    assert TomlConfigClass.dict_var == {"key": "value"}
    assert TomlConfigClass.int_var == 5


@pytest.mark.skipif(
    sys.version_info >= (3, 11),
    reason="'tomllib' is available by default for python with version >= 3.11",
)
def test_toml_config_format_tomli_ok():
    @properties(filename="application.toml")
    class TomlConfigClass(BaseClass):
        pass

    assert TomlConfigClass.list_var == ["a", "b", "c"]
    assert TomlConfigClass.dict_var == {"key": "value"}
    assert TomlConfigClass.int_var == 5


def test_toml_config_format_not_found_any_toml_parser():
    with patch("conjector.config_handler.tomllib", None), patch(
        "conjector.config_handler.tomli", None
    ):
        with pytest.raises(ImportError):

            @properties(filename="application.toml")
            class TomlConfigClass(BaseClass):
                pass


def test_json_config_format_ujson_ok():
    @properties(filename="application.json")
    class UJsonConfigClass(BaseClass):
        pass

    assert UJsonConfigClass.list_var == ["a", "b", "c"]
    assert UJsonConfigClass.dict_var == {"key": "value"}
    assert UJsonConfigClass.int_var == 5


def test_json_config_format_default_parser():
    with patch("conjector.config_handler.ujson", None):

        @properties(filename="application.json")
        class JsonConfigClass(BaseClass):
            pass

        assert JsonConfigClass.list_var == ["a", "b", "c"]
        assert JsonConfigClass.dict_var == {"key": "value"}
        assert JsonConfigClass.int_var == 5


def test_ini_config_format_default_parser():
    @properties(filename="application.ini")
    class IniConfigClass(BaseClass):
        pass

    assert IniConfigClass.list_var == ["a", "b", "c"]
    assert IniConfigClass.dict_var == {"key": "value"}
    assert IniConfigClass.int_var == 5
