from typing import Tuple

import pytest

from app_properties import properties


class Base:
    bool_bool_vars: Tuple[bool, bool]
    int_bool_vars: Tuple[bool, bool]
    str_bool_vars: Tuple[bool, bool]
    wrong_bool_vars: Tuple[bool, bool]


@pytest.fixture
def boolean_class_fixt():
    @properties(
        filename="tests/types_cast.yml", type_cast=True, root="boolean"
    )
    class BooleanClass(Base):
        pass

    return BooleanClass


def test_cast_boolean_vars(boolean_class_fixt):
    expected_booleans = (True, False)
    assert boolean_class_fixt.bool_bool_vars == expected_booleans
    assert boolean_class_fixt.int_bool_vars == expected_booleans
    assert boolean_class_fixt.str_bool_vars == expected_booleans
    assert boolean_class_fixt.wrong_bool_vars == (None, None)