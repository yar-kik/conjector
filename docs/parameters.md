# Decorator parameters

The main functional component of the library is the `@properties` decorator, which, like the `@dataclass` decorator, can be used with or without brackets, so the following class definitions are similar:
```{literalinclude} examples/with_and_without_brackets.py
```
Each decorator parameter can be overridden using a [global configuration](global_settings.md) file.

## Config filename 
`filename` - the name of a file with config. By default, it is `application.yml`. 
For now, `yaml`, `json` and `toml` [config formats](config_formats.md) are fully supported, `ini` is supported but with some limitations.
Config file will be searched in the same directory where is file with used decorator. Use a relative path to read the file from a parent directory.

Suppose we have the following project structure:
```
<project_root>
|---services
|   |   email_message_service.py
|   |   auth_service.py
|   |   .....
|---configs
|   |   service_config.toml
|   |   .....
```
Our file with the constants is located in the `configs` directory, and a class that uses these values is in `email_message_service.py` which is located in the `services` directory. Then the path to the file will be written as follows - `filename="../configs/service_config.toml"`

## Disabling type casting
`type_cast` - used to know whether you want to cast config values to the field type. 
By default, it's `True`, which means values in a config file will be cast according to the type hints. All types specified in the section [supported types](supported_types.md) will be available for type casting. Also, nested types will be recursively cast.
If `False`, type hinting is ignored, and available types are limited by a file format:

| Python   | JSON | YAML | TOML | INI |
|----------|------|------|------|-----|
| str      | +    | +    | +    | +   |
| int      | +    | +    | +    | -   |
| float    | +    | +    | +    | -   |
| bool     | +    | +    | +    | -   |
| none     | +    | +    | +    | -   |
| dict     | +    | +    | +    | +   |
| list     | +    | +    | +    | +   |
| datetime | -    | -    | +    | -   |


## Override default params
`override_default` - used to know whether you want to override the default values of class variables. By default, it is `False`.


## Enable lazy initialization
`lazy_init` - used to know whether you want to set config values immediately on the application start-up or on demand ("lazily") after calling the method `init_props()`. By default, it is `False`. For more details read section [lazy initialization](lazy_initialization.md)

## Specify root path of config
`root` - root key in the config. It's the way to create "namespaces" when you work with multiple classes but use a single config file. It could be a nested value with separation by dots, for example:

`example.yml`:
```{literalinclude} examples/example.yml
```

`services.py`:
```{literalinclude} examples/root_param.py
```
