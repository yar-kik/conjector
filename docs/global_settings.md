# Global settings

This library also supports global file settings (like `pytest` or `flake`). 
So, you can override some parameters, which are passed to the decorator if default values aren't ok for you.
For example, if you want to have the default config filename `my-app.toml` and 
don't write every time `@properties(filename="my-app.toml")`, 
just add the next lines in `pyproject.toml` in your project root:
```toml
[tool.conjector]
filename = "my-app.toml"
```
And now you can use just bare decorator without parenthesis:
```python
@properties
class MyClass:
    ...
```
Also, `conjector` can work with the `tox.ini`:
```ini
[conjector]
filename = my-default-config.ini
```
And `setup.cfg`: 
```ini
[tool:conjector]
filename = new-filename.yaml
``` 
So, you must put your options under the appropriate sections.

```{note} 
`ini` config format doesn't support list with dicts or other lists, like `list[list[int]]` or `list[dict[str, Any]]`. 
Only primitive types (`int`, `float`, `str`, `bool` and `null`) are available.  
```
