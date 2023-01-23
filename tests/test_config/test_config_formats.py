import pytest
import sys
from unittest.mock import patch

from app_properties import properties


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
    assert YamlConfigClass.int_var == 12


def test_yaml_config_format_with_pyloader():
    with patch.dict(sys.modules["yaml"].__dict__) as patched_yaml:
        del patched_yaml["CSafeLoader"]

        @properties(filename="application.yml")
        class YamlConfigClass(BaseClass):
            pass

        assert YamlConfigClass.list_var == ["a", "b", "c"]
        assert YamlConfigClass.dict_var == {"key": "value"}
        assert YamlConfigClass.int_var == 12


def test_yaml_config_format_pyyaml_not_found():
    with patch("app_properties.config_handler.yaml", None):
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
    assert TomlConfigClass.int_var == 12


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
    assert TomlConfigClass.int_var == 12


@pytest.mark.skipif(
    sys.version_info >= (3, 11),
    reason="'tomllib' is available by default for python with version >= 3.11",
)
def test_toml_config_format_toml_ok():
    with patch("app_properties.config_handler.tomli", None):

        @properties(filename="application.toml")
        class TomlConfigClass(BaseClass):
            pass

        assert TomlConfigClass.list_var == ["a", "b", "c"]
        assert TomlConfigClass.dict_var == {"key": "value"}
        assert TomlConfigClass.int_var == 12


def test_toml_config_format_not_found_any_toml_parser():
    with patch("app_properties.config_handler.tomllib", None), patch(
        "app_properties.config_handler.tomli", None
    ), patch("app_properties.config_handler.toml", None):
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
    assert UJsonConfigClass.int_var == 12


def test_json_config_format_default_parser():
    with patch("app_properties.config_handler.ujson", None):

        @properties(filename="application.json")
        class JsonConfigClass(BaseClass):
            pass

        assert JsonConfigClass.list_var == ["a", "b", "c"]
        assert JsonConfigClass.dict_var == {"key": "value"}
        assert JsonConfigClass.int_var == 12
