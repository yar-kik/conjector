# Lazy initialization

If you want to create some class instance with filled required data during init, 
and then populated with config values, you can use the parameter `lazy_init` for this purpose.
All file constants will be injected after calling the method `init_props`. Example of work:

`application.yml`:
```{literalinclude} examples/application.yml
```

`lazy_init_demo.py`:
```{literalinclude} examples/lazy_init_param.py
```

Because there are 3 sources of data (default values, values passed during initialization, and config file values), 
it could be hard to understand how we can resolve this conflict.
Bellow is the table to clarify the behavior of the `init_props` method.

| init     | default | config | will be used  |
|----------|---------|--------|---------------|
| -        | +       | -      | default       |
| -        | +       | +      | config        |
| +        | ~       | -      | init          |
| +        | ~       | +      | init \ config |

_`+`- provided; `-`- missing; `~`- not affect._

How you can see, when both `init` and `config` values provided, they are equally important,
but, by default, `config` have higher priority and overrides `init`. 
If you, for some reason, don't want to override already initialized values, only defaults,
it's also possible with `init_props(override_init=False)`
