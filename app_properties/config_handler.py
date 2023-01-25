from typing import Any, Callable, Dict, List, TypeVar

import configparser
import functools
import inspect
import json
import pathlib
import sys
import warnings
from os.path import dirname, join, normpath, sep

if sys.version_info >= (3, 11):
    import tomllib
else:
    tomllib = None  # type: ignore

try:
    import tomli
except ImportError:
    tomli = None

try:
    import toml
except ImportError:
    toml = None  # type: ignore

try:
    import ujson
except ImportError:
    ujson = None  # type: ignore

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")


class ConfigHandler:
    supported_configs = ("pyproject.toml",)

    def __init__(self) -> None:
        self._caller_dir = self._get_caller_directory()

    def get_config(
        self, filename: str, *, ignore_case: bool, root: str
    ) -> dict:
        file = self._get_config_file(filename)
        raw_config = self._resolve_config_format(file)
        return self._process_config(raw_config, ignore_case, root)

    def get_global_settings(self) -> dict:
        project_root = self._get_project_root()
        for config_type in self.supported_configs:
            file = project_root / config_type
            if not file.exists():
                continue
            try:
                config = self._resolve_config_format(file)
            except ImportError as e:
                warnings.warn(
                    f"{e} Ignoring global settings...", ImportWarning
                )
                config = {}
            if config_type == "pyproject.toml":
                config = config.get("tool", {}).get("conjector", {})
            return config
        return {}

    def _get_project_root(self) -> pathlib.Path:
        directory = pathlib.Path(self._caller_dir)
        while (directory / "__init__.py").exists():
            directory = directory.parent
        return directory

    def _get_caller_directory(self) -> str:
        stack = inspect.stack()
        stack_depth = 0
        for i, frame in enumerate(stack, 1):
            if frame.filename.split(sep)[-2:] == ["app_properties", "main.py"]:
                stack_depth = i
        return dirname(stack[stack_depth].filename)

    def _resolve_config_format(self, file: pathlib.Path) -> dict:
        text_content = file.read_text()
        if file.suffix in (".yml", ".yaml"):
            conf = self._get_yaml_config(text_content)
        elif file.suffix == ".json":
            conf = self._get_json_config(text_content)
        elif file.suffix == ".toml":
            conf = self._get_toml_config(text_content)
        elif file.suffix == ".ini":
            conf = self._get_ini_config(text_content)
        else:
            raise NotImplementedError("Specified config type isn't supported!")
        return conf

    def _get_config_file(self, filename: str) -> pathlib.Path:
        abs_config_path = join(self._caller_dir, normpath(filename))
        file = pathlib.Path(abs_config_path)
        if not file.exists():
            raise FileNotFoundError(f"File '{file.name}' is not found!")
        return file

    def _get_yaml_config(self, text_content: str) -> dict:
        if yaml is None:
            raise ImportError(
                '"PyYAML" is not installed, run `pip install conjector[yaml]`'
            )
        try:
            SafeLoader = yaml.CSafeLoader
        except AttributeError:
            SafeLoader = yaml.SafeLoader  # type: ignore
        # equivalent of yaml.safe_load() but could be faster with CSafeLoader
        return yaml.load(text_content, SafeLoader)  # nosec

    def _get_json_config(self, text_content: str) -> dict:
        if ujson is not None:
            return ujson.loads(text_content)
        warnings.warn(
            "Using built-in library for JSON parsing. "
            "It's recommended to use another library for this purpose. "
            "To install run `pip install conjector[json]`",
            UserWarning,
        )
        return json.loads(text_content)

    def _get_toml_config(self, text_content: str) -> dict:
        if tomllib is not None:
            return tomllib.loads(text_content)
        if tomli is not None:
            return tomli.loads(text_content)
        if toml is not None:
            warnings.warn(
                'Using "toml" library is deprecated. '
                'It\'s recommended to use "tomli" instead. '
                "To install run `pip install conjector[toml]`",
                DeprecationWarning,
            )
            return toml.loads(text_content)
        raise ImportError(
            '"tomli" is not installed, run `pip install conjector[toml]`'
        )

    def _get_ini_config(self, text_content: str) -> dict:
        parser = configparser.ConfigParser(strict=False)
        parser.read_string(text_content)
        parsed_result: Dict[str, Any] = {}
        for section in parser.sections():
            for key in parser[section]:
                subsections = section.split(".") + [key]
                self._set_nested_item(
                    parsed_result, subsections, parser[section][key]
                )
        return parsed_result

    def _set_nested_item(
        self, mapping: dict, keys: List[str], value: str
    ) -> None:
        if keys[0].lower() == "root":
            keys = keys[1:]
        if keys[-1].endswith("[]"):
            keys[-1] = keys[-1][:-2]
            value = value.split(",")  # type: ignore
        for i in range(1, len(keys) + 1):
            pointer = mapping
            for j in range(i):
                if keys[j] in pointer:
                    pointer = pointer[keys[j]]
                else:
                    pointer[keys[j]] = {} if i != len(keys) else value

    def _apply_to_key(
        self, mapping: Dict[_K, _V], func: Callable[[_K], _T]
    ) -> Dict[_T, _V]:
        return {func(k): mapping[k] for k in mapping}

    def _process_config(
        self, config: dict, ignore_case: bool, root: str
    ) -> dict:
        config = self._apply_to_key(config, lambda x: str.replace(x, "-", "_"))
        if ignore_case:
            config = self._apply_to_key(config, str.lower)
        else:
            warnings.warn(
                "Parameter `ignore_case` is deprecated. "
                "It'll be removed in the future releases.",
                DeprecationWarning,
            )
        if root:
            config = functools.reduce(
                lambda x, y: x[y], root.split("."), config
            )
        return config
