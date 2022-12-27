from typing import FrozenSet, Set

import pytest

from app_properties import properties


class BaseClass:
    unspecified_set_var: set
    unspecified_frozenset_var: frozenset
    int_set_var: Set[int]
    int_frozenset_var: FrozenSet[int]


@pytest.fixture
def set_class_fixt(request):
    @properties(filename=request.param, root="set")
    class SetClass(BaseClass):
        pass

    return SetClass


@pytest.mark.parametrize(
    "set_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml"),
    indirect=True,
)
def test_field_with_set(set_class_fixt):
    assert set_class_fixt.int_set_var == {1, 2, 3}
    assert set_class_fixt.int_frozenset_var == frozenset([4, 5, 6])
    assert set_class_fixt.unspecified_set_var == {"10", "20", "30"}
    assert set_class_fixt.unspecified_frozenset_var == frozenset(
        ["40", "50", "60"]
    )
