from app_properties.dtos import DEFAULT, Settings


def test_merge_user_params_with_custom_settings():
    user_params = Settings(filename=DEFAULT)
    custom = Settings(filename="custom_config.toml")
    assert user_params | custom == custom | user_params
    assert (user_params | custom).filename == "custom_config.toml"


def test_merge_user_params_with_default_settings():
    user_params = Settings(filename=DEFAULT)
    default = Settings()
    assert user_params | default == default | user_params
    assert (user_params | default).filename == "application.yml"


def test_merge_default_with_custom_settings():
    default = Settings()
    custom = Settings(filename="custom_config.toml")
    assert default | custom != custom | default
    assert (default | custom).filename == "custom_config.toml"
    assert (custom | default).filename == "application.yml"


def test_merge_two_different_settings():
    first = Settings(filename="first_application.yml")
    second = Settings(filename="second_application.yml")
    assert first | second != second | first
    assert (first | second).filename == "second_application.yml"
    assert (second | first).filename == "first_application.yml"
