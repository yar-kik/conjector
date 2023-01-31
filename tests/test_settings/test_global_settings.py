import pytest
from unittest.mock import patch

from app_properties import Conjector, properties
from app_properties.config_handler import ConfigHandler
from app_properties.dtos import Settings


class BaseClass:
    some_str_var: str
    some_default_int_var: int = 10


@pytest.fixture
def default_params_fixt():
    with patch.object(
        ConfigHandler,
        "supported_config_mapping",
        {"pyproject.toml": ("tool", "conjector")},
    ):

        @properties
        class DefaultParamsClass(BaseClass):
            pass

    return DefaultParamsClass


@pytest.fixture
def decorator_params_fixt():
    with patch.object(
        ConfigHandler,
        "supported_config_mapping",
        {"pyproject.toml": ("tool", "conjector")},
    ):

        @properties(filename="decorator_config.yml", override_default=False)
        class UserParamsClass(BaseClass):
            pass

    return UserParamsClass


def test_global_settings_override_default(default_params_fixt):
    assert default_params_fixt.some_str_var == "global settings"
    assert default_params_fixt.some_default_int_var == 20


def test_decorator_params_override_global_settings(decorator_params_fixt):
    assert decorator_params_fixt.some_str_var == "decorator params"
    assert decorator_params_fixt.some_default_int_var == 10


@pytest.mark.parametrize(
    "config_formats,expected_config",
    [
        ({"not_existing.cnfg": ("conjector",)}, Settings()),
        ({}, Settings()),
        (
            {"pyproject.toml": ("tool", "conjector")},
            Settings(
                filename="pyproject_toml_config.yml", override_default=True
            ),
        ),
        (
            {"tox.ini": ("conjector",)},
            Settings(filename="tox_ini_config.yml", override_default=True),
        ),
        (
            {"setup.cfg": ("tool:conjector",)},
            Settings(filename="setup_cfg_config.yml", override_default=True),
        ),
    ],
)
def test_settings_file_format(config_formats, expected_config):
    with patch.object(
        ConfigHandler, "supported_config_mapping", config_formats
    ):
        config_handler = Conjector()
        global_settings = config_handler._get_global_settings()
        assert global_settings == expected_config
