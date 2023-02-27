from conjector import Default, properties


@properties(filename="function_defaults.yml", root="some_func_scope")
def first_func(
    required: int,
    regular_default: int = 20,
    specified_default: int = Default(30),
    file_default: int = Default(),
):
    return required, regular_default, specified_default, file_default


assert first_func(10, 20, 30, 40) == (10, 20, 30, 40)
assert first_func(10) == (10, 20, 33, 44)


@properties(filename="function_defaults.yml", root="not_existing_func_scope")
def second_func(
    required: int,
    regular_default: int = 20,
    specified_default: int = Default(30),
    file_default: int = Default(),
):
    return required, regular_default, specified_default, file_default


assert second_func(10, 20, 30, 40) == (10, 20, 30, 40)
assert second_func(10) == (10, 20, 30, 0)
