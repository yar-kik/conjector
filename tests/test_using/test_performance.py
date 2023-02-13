from unittest.mock import patch

from conjector import properties
from conjector.config_handler import ConfigHandler


@patch.object(ConfigHandler, "get_global_settings")
@patch.object(ConfigHandler, "_parse_yaml_config")
def test_decorator_for_class_will_read_same_config_once(
    mocked_get_config, mocked_get_global_settings
):
    mocked_get_config.return_value = {"a": 10, "b": 20}
    mocked_get_global_settings.return_value = {}

    @properties(filename="application.yml")
    class FirstClass:
        pass

    @properties(filename="application.yml")
    class SecondClass:
        pass

    mocked_get_config.assert_called_once()


@patch.object(ConfigHandler, "get_global_settings")
@patch.object(ConfigHandler, "_parse_yaml_config")
def test_decorator_for_func_will_read_same_config_once(
    mocked_get_config, mocked_get_global_settings
):
    mocked_get_config.return_value = {"a": 10, "b": 20}
    mocked_get_global_settings.return_value = {}

    @properties(filename="application.yml")
    def func():
        pass

    func()
    func()

    mocked_get_config.assert_called_once()
