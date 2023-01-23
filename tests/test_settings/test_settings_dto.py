from app_properties.dtos import Settings


def test_merge_default_with_custom_settings():
    default = Settings()
    custom = Settings(filename="custom_config.toml")
    merged = default | custom
    assert default | custom == custom | default
    assert merged.filename == "custom_config.toml"


def test_merge_two_different_settings():
    first = Settings(filename="first_application.yml")
    second = Settings(filename="second_application.yml")
    assert first | second != second | first
    assert (first | second).filename == "second_application.yml"
    assert (second | first).filename == "first_application.yml"
