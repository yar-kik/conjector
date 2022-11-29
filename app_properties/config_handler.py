from typing import Callable, Dict, TypeVar

import functools
import inspect
import json
import pathlib
import yaml
from os.path import dirname, join, normpath, sep

_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")


class ConfigHandler:
    def __init__(self, config_name: str) -> None:
        self._conf_name = config_name
        self._caller_dir = self._get_caller_directory()

    def get_config(self, ignore_case: bool, root: str) -> dict:
        file = self._get_config_file()
        raw_config = self._resolve_config_format(file)
        return self._process_config(raw_config, ignore_case, root)

    def _get_caller_directory(self) -> str:
        stack = inspect.stack()
        stack_depth = 3
        # if used decorator without parens:
        if stack[stack_depth].filename.split(sep)[-2:] == [
            "app_properties",
            "main.py",
        ]:
            stack_depth = 4
        return dirname(stack[stack_depth].filename)

    def _resolve_config_format(self, file: pathlib.Path) -> dict:
        text_content = file.read_text()
        if file.suffix in (".yml", ".yaml"):
            conf = self._get_yaml_config(text_content)
        elif file.suffix == ".json":
            conf = self._get_json_config(text_content)
        else:
            raise NotImplementedError("Specified config type isn't supported!")
        return conf

    def _get_config_file(self) -> pathlib.Path:
        abs_config_path = join(self._caller_dir, normpath(self._conf_name))
        file = pathlib.Path(abs_config_path)
        if not file.exists():
            raise FileNotFoundError(f"File '{file.name}' is not found!")
        return file

    def _get_yaml_config(self, text_content: str) -> dict:
        return yaml.load(text_content, yaml.CSafeLoader)

    def _get_json_config(self, text_content: str) -> dict:
        return json.loads(text_content)

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
        if root:
            config = functools.reduce(
                lambda x, y: x[y], root.split("."), config
            )
        return config
