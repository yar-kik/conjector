# Function defaults

Using `conjector` you can not only inject config values into class, but also into function defaults.
Let's start by taking a look at an example. The code below demonstrates how to use `conjector` 
to specify function defaults with values that can be replaced by configuration values:

`function_defaults.yml`:
```{literalinclude} examples/function_defaults.yml
```

`function_defaults.py`:
```{literalinclude} examples/function_defaults.py
```


The `required` parameter is a required function argument, while the other parameters have default values. 
The `specified_default` parameter uses the `Default` wrapper to indicate that its value can be replaced 
by a value from the configuration file. The `file_default` parameter also uses the `Default` wrapper, 
but with an empty value, which means it will use the default value of its type.

The assert statements verify that the functions return the expected output for various input parameters. 
If all arguments are provided, the functions use the provided values, including any that replace `Default` markers. 
If any arguments are missing, the functions will use the configuration values, if available, or the default values otherwise.

## Wrapping class methods
With `@properties` decorator under class, you can also use `Default` marker in every method:
```python
@properties
class OtherClass:
    def __init__(self, a: int = Default(), b: int = Default()) -> None:
        self.a = a
        self.b = b

    def simple_method(
        self, a: int = Default(), b: int = Default()
    ) -> Tuple[int, int]:
        return a, b

    @classmethod
    def cls_method(
        cls, a: int = Default(), b: int = Default()
    ) -> Tuple[int, int]:
        return a, b

    @staticmethod
    def stat_method(
        a: int = Default(), b: int = Default()
    ) -> Tuple[int, int]:
        return a, b
```
So there is no need to wrapp every method with `properties` decorator. 
But "magic methods" (except `__init__`) are unwrapped by default.
