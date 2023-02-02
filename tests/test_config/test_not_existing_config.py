import pytest

from conjector import properties


def test_config_not_found():
    with pytest.raises(FileNotFoundError):

        @properties(filename="not_existing.yml")
        class NotFoundClass:
            value1: int
            value2: str
