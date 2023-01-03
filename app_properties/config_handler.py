from typing import Callable, Dict, TypeVar

import functools
import inspect
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
    import ujson as json
except ImportError:
    import json  # type: ignore

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")


class ConfigHandler:
    def __init__(self) -> None:
        self._caller_dir = self._get_caller_directory()

    def get_config(
        self, filename: str, *, ignore_case: bool, root: str
    ) -> dict:
        file = self._get_config_file(filename)
        raw_config = self._resolve_config_format(file)
        return self._process_config(raw_config, ignore_case, root)

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
        return json.loads(text_content)

    def _get_toml_config(self, text_content: str) -> dict:
        if tomllib is not None:
            return tomllib.loads(text_content)
        if tomli is not None:
            return tomli.loads(text_content)
        if toml is not None:
            warnings.warn(
                'Using "toml" library is deprecated. '
                'It\'s recommended to use "tomli" instead.'
                "To install run `pip install conjector[toml]`",
                DeprecationWarning,
            )
            return toml.loads(text_content)
        raise ImportError(
            '"tomli" is not installed, run `pip install conjector[toml]`'
        )

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
