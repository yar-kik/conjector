from typing import Optional

from conjector import properties


@properties(filename="optional_types.yml")
class SomeOptionalClass:
    optional_value_presented: Optional[int]
    optional_value_missing: Optional[int]
    optional_value_invalid: Optional[int]


assert SomeOptionalClass.optional_value_presented == 10
assert SomeOptionalClass.optional_value_missing is None
assert SomeOptionalClass.optional_value_invalid is None
