import pytest
from decimal import Decimal

from conjector import properties


@pytest.fixture
def decimal_class_fixt(request):
    @properties(filename=request.param, root="decimal")
    class DecimalClass:
        int_decimal_var: Decimal
        float_decimal_var: Decimal
        str_decimal_var: Decimal
        missing_decimal_var: Decimal

    return DecimalClass


@pytest.mark.parametrize(
    "decimal_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_decimal_field_ok(decimal_class_fixt):
    assert decimal_class_fixt.int_decimal_var == Decimal("10")
    assert decimal_class_fixt.float_decimal_var == Decimal("12.5")
    assert decimal_class_fixt.str_decimal_var == Decimal("15.150")
    assert decimal_class_fixt.missing_decimal_var == Decimal()


@pytest.mark.parametrize(
    "filename",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
)
def test_invalid_decimal_field(filename):
    with pytest.raises(ValueError):

        @properties(filename=filename, root="decimal")
        class GeneralInvalidDecimalClass:
            general_invalid_decimal_var: Decimal
