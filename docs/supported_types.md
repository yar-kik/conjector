# Supported types

`conjector` can work with deep nested data structures and recursively cast them to corresponding type hints.
The table below shows how config values (`json` syntax example) are cast to Python types:

| Python type                                  | Config file type                                           | Config example                                                                                                                                                 |
|----------------------------------------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `int`                                        | `int`<br/>`str`                                            | `10`<br/>`"10"`                                                                                                                                                |
| `float`                                      | `float`<br/>`int`<br/>`str`                                | `10.5`<br/>`10`<br/>`"10.5"`                                                                                                                                   |
| `str`                                        | `str`                                                      | `"string value"`                                                                                                                                               |
| `bool`                                       | `bool`<br/>`int`<br/>`str`                                 | `true` / `false`<br/>`1` / `0`<br/>`"True"` / `"False"`, `"true"` / `"false"`                                                                                  |
| `None`                                       | `null`                                                     | `null`                                                                                                                                                         |
| `dict`                                       | `dict`                                                     | `{"key": "value"}`                                                                                                                                             |
| `list`<br/>`tuple`<br/>`set`<br/>`frozenset` | `list`                                                     | `["val1", "val2"]`                                                                                                                                             |
| `TypedDict`                                  | `dict`                                                     | `{"str_var": "value"}`                                                                                                                                         |
| `NamedTuple`                                 | `list`<br/>`dict`                                          | `["value", 10]`<br/>`{"str_val": "value", "int_val": 10}`                                                                                                      |
| `dataclass`                                  | `dict`                                                     | `{"str_val": "str", "int_val": 10}`                                                                                                                            |
| `datetime.datetime`                          | `str`<br/>`int`<br/>`list`<br/>`dict`                      | `"2022-12-11T10:20:23"`<br/>`1670754600`<br/>`[2022, 12, 11, 10, 20, 23]`<br/>`{"year": 2022, "month": 12, "day": 11, "hour": 10, "minute": 20, "second": 23}` |
| `datetime.date`                              | `str`<br/>`list`<br/>`dict`                                | `"2022-12-11"`<br/>`[2022, 12, 11]`<br/>`{"year": 2022, "month": 12, "day": 11}`                                                                               |
| `datetime.time`                              | `str`<br/>`list`<br/>`dict`                                | `"12:30:02"`<br/>`[12, 30, 2]`<br/>`{"hour": 12, "minute": 30, "second": 2}`                                                                                   |
| `datetime.timedelta`                         | `dict`                                                     | `{"days": 1, "hours": 2, "minutes": 10}`                                                                                                                       |
| `enum.Enum`                                  | `str`<br/>`int`                                            | `"VALUE"`<br/>`10`                                                                                                                                             |
| `re.Pattern`                                 | `str`                                                      | `"\w+"`                                                                                                                                                        |
| `decimal.Decimal`                            | `str`<br/>`int`<br/>`float`<br/>`list[int, list[int], int` | `"12.150"`<br/>`100`<br/>`12.5`<br/>`[1, [1, 2, 5], -3]`                                                                                                       |
| `pathlib.Path`                               | `str`                                                      | `"some/path/to/file.txt"`/`"some/path/to/dir/"`                                                                                                                |

## Optional types
The default behavior for the `Optional` type hint: try to convert the value to a specified type, if successful - use the converted value, else use None. Also, None will be used if no value is provided.

`optional_types.yml`
```{literalinclude} examples/optional_types.yml
```

`optional_types.py`:
```{literalinclude} examples/optional_types.py
```


## Union types
How the Union type hint works: in a specified order (e.g. `Union[float, dict, str]`) the value will be cast first to `float`, then, if the attempt fails, to `dict`, and finally to `str`. If the value cannot be converted to any of the provided types, `ValueError` will be thrown. The casting process will be stopped immediately after the first successful attempt.

`union_types.yml`:
```{literalinclude} examples/union_types.yml
```

`union_types.py`:
```{literalinclude} examples/union_types.py
```
