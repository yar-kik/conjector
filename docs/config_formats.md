# Config formats

## JSON and YAML
These two types are equivalent in terms of supported data types, but the author of `conjector` is more inclined to `yaml` when it comes to usability and readability. Also, `yaml` has such interesting things as aliases and anchors, which can simplify the work with constants even more.

However, in terms of speed, `yaml` loses even to the built-in `json` library, not to mention the faster version of `ujson`. Therefore, for large configurations, it is recommended to use the `json` format. 

Also, you should keep in mind that reading configs and injecting values occurs only once at the beginning of your application, so you can neglect the performance to a certain extent.

## TOML
The `toml` format supports all the same types as `json` and `yaml`, and since version "1.0.0", it can work with arrays whose elements have different types. However, there is still a problem when the array contains the value `null`. 
Consider the situation when we have a variable with the following type annotation - `list[int | str | None]`. Then we can write it in the following ways:
1) Use the value null written as a string:
    ```toml
   [some_section]
    some_var = ["str", 10, "null"]
    ```
2) Use any invalid value (but it's more like hack):
    ```toml
   [some_section]
    some_var = ["str", 10, {}]
    ```

## INI
By default, `configparser.ConfigParser` doesn't support lists and deep nested dicts, 
but `conjector` makes it possible to work with them. How does it look?

__Python code:__
```python
{
    "some_key": {
        "another_key": "value",
        "deep_key": {
            "key1": True,
            "key2": None,
        }
    },
    "just_key": 10,
    "mixed_list": [10, "20", 30.5, None]
}
```
__`.ini` config__
```ini
[some_key]
another_key = "value"
[some_key.deep_key]
key1 = true
key2 = null
[root]
just_key = 10
mixed_list[] = 10,20,30.5,null
```
As you can see above, a list in a `.ini` config is coma-separated values where a key has a suffix `[]` in the end. 
The dict nesting is also trivial, all you need is just dot-separated keys of nested dicts in `[section]` part.
Also, you should remember that `configparser` can't work with variables without sections, so if you want to put
some values in the root of a config just write a section `[root]` (or `[ROOT]`) above, like in the previous example.
