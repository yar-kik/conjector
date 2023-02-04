from typing import List, Union

from conjector import properties


@properties(filename="union_types.yml")
class SomeUnionClass:
    union_value_float: Union[float, dict, str]
    union_value_dict: Union[float, dict, str]
    union_value_str: Union[float, dict, str]

    union_values_dict: Union[dict, List[dict]]
    union_values_list: Union[dict, List[dict]]


assert SomeUnionClass.union_value_float == 125
assert SomeUnionClass.union_value_dict == {"key": "value"}
assert SomeUnionClass.union_value_str == "str value"
assert SomeUnionClass.union_values_dict == {"some": "value"}
assert SomeUnionClass.union_values_list == [{"some": "val1"}, {"some": "val2"}]
