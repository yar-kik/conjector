from typing import Any, Callable, Dict, List, Optional, TypeVar

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
    supported_config_mapping = {
        "pyproject.toml": ("tool", "conjector"),
        "tox.ini": ("conjector",),
        "setup.cfg": ("tool:conjector",),
    }
    parsed_configs_map: Dict[pathlib.Path, Dict[str, Any]] = {}

    def __init__(self) -> None:
        self._caller_dir = self._get_caller_directory()

    def get_config(self, filename: str, *, root: str) -> dict:
        path = self._get_config_path(filename)
        raw_config = self.parse_config(path)
        return self._process_config(raw_config, root)

    def get_global_settings(self) -> dict:
        project_root = self._get_project_root()
        for config_type, sections in self.supported_config_mapping.items():
            file = project_root / config_type
            if not file.exists():
                continue
            try:
                config = self.parse_config(file)
            except ImportError as e:
                warnings.warn(
                    f"{e} Ignoring global settings...", ImportWarning
                )
                config = {}
            config = functools.reduce(
                lambda x, y: x.get(y, {}), sections, config
            )
            return config
        return {}

    def parse_config(self, file_path: pathlib.Path) -> dict:
        if conf := self.parsed_configs_map.get(file_path):
            return conf
        text_content = file_path.read_text()
        if file_path.suffix in (".yml", ".yaml"):
            conf = self._parse_yaml_config(text_content)
        elif file_path.suffix == ".json":
            conf = self._parse_json_config(text_content)
        elif file_path.suffix == ".toml":
            conf = self._parse_toml_config(text_content)
        elif file_path.suffix in (".ini", ".cfg"):
            conf = self._parse_ini_config(text_content)
        else:
            raise NotImplementedError("Specified config type isn't supported!")
        self.parsed_configs_map[file_path] = conf
        return conf

    @classmethod
    def clear_cache(cls, path: Optional[pathlib.Path] = None) -> None:
        if path:
            cls.parsed_configs_map.pop(path, None)
        else:
            cls.parsed_configs_map.clear()

    def _get_project_root(self) -> pathlib.Path:
        directory = pathlib.Path(self._caller_dir)
        while (directory / "__init__.py").exists():
            directory = directory.parent
        return directory

    def _get_caller_directory(self) -> str:
        stack = inspect.stack()
        stack_depth = 0
        for i, frame in enumerate(stack, 1):
            if frame.filename.split(sep)[-2:] == ["conjector", "main.py"]:
                stack_depth = i
        return dirname(stack[stack_depth].filename)

    def _get_config_path(self, filename: str) -> pathlib.Path:
        abs_config_path = join(self._caller_dir, normpath(filename))
        file = pathlib.Path(abs_config_path)
        if not file.exists():
            raise FileNotFoundError(f"File '{file.name}' is not found!")
        return file

    def _parse_yaml_config(self, text_content: str) -> dict:
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

    def _parse_json_config(self, text_content: str) -> dict:
        if ujson is not None:
            return ujson.loads(text_content)
        warnings.warn(
            "Using built-in library for JSON parsing. "
            "It's recommended to use another library for this purpose. "
            "To install run `pip install conjector[json]`",
            UserWarning,
        )
        return json.loads(text_content)

    def _parse_toml_config(self, text_content: str) -> dict:
        if tomllib is not None:
            return tomllib.loads(text_content)
        if tomli is not None:
            return tomli.loads(text_content)
        raise ImportError(
            '"tomli" is not installed, run `pip install conjector[toml]`'
        )

    def _parse_ini_config(self, text_content: str) -> dict:
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

    def _process_config(self, config: dict, root: str) -> dict:
        config = self._apply_to_key(config, lambda x: str.replace(x, "-", "_"))
        if root:
            config = functools.reduce(
                lambda x, y: x[y], root.split("."), config
            )
        return {} if config is None else config
