from typing import List

import pytest

from app_properties import properties


class BaseClass:
    unspecified_list_var: list
    int_list_var: List[int]


@pytest.fixture
def list_class_fixt():
    @properties(filename="types_cast.yml", root="list")
    class ListClass(BaseClass):
        pass

    return ListClass


def test_field_with_list(list_class_fixt):
    assert list_class_fixt.int_list_var == [1, 2, 3]
    assert list_class_fixt.unspecified_list_var == ["10", "20", "30"]
