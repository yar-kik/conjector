from conjector import properties


@properties
class FirstClass:
    pass


@properties()
class SecondClass:
    pass


@properties(
    filename="application.yml",
    override_default=False,
    root="",
    type_cast=True,
    lazy_init=False,
)
class ThirdClass:
    pass
