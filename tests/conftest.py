from typing import Any, Dict

from unittest.mock import Mock, patch


def patch_config(return_values: Dict[str, Any]):
    from conjector.config_handler import ConfigHandler

    return patch.object(
        ConfigHandler, "get_config", Mock(return_value=return_values)
    )
