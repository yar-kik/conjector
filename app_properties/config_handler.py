from typing import Callable, Dict, TypeVar

import functools
import json
import logging
import pathlib
import yaml

_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")

logger = logging.getLogger(__name__)


def get_config(conf_name: str, ignore_case: bool, root: str) -> dict:
    raw_config = _read_config(conf_name)
    return _process_config(raw_config, ignore_case, root)


def _read_config(conf_name: str) -> dict:
    file = pathlib.Path(conf_name)
    if not file.exists():
        logger.warning(f"File {file} was not found. Using default values...")
        return {}
    text_content = file.read_text()
    if conf_name.endswith(".yml") or conf_name.endswith(".yaml"):
        conf = _get_yaml_config(text_content)
    elif conf_name.endswith(".json"):
        conf = _get_json_config(text_content)
    else:
        raise NotImplementedError("Specified config type isn't supported!")
    return conf


def _get_yaml_config(text_content: str) -> dict:
    return yaml.load(text_content, yaml.CSafeLoader)


def _get_json_config(text_content: str) -> dict:
    return json.loads(text_content)


def _apply_to_key(
    mapping: Dict[_K, _V], func: Callable[[_K], _T]
) -> Dict[_T, _V]:
    return {func(k): mapping[k] for k in mapping}


def _process_config(config: dict, ignore_case: bool, root: str) -> dict:
    config = _apply_to_key(config, lambda x: str.replace(x, "-", "_"))
    if ignore_case:
        config = _apply_to_key(config, str.lower)
    if root:
        config = functools.reduce(lambda x, y: x[y], root.split("."), config)
    return config
