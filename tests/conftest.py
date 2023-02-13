from typing import Any, Dict

import pytest
from unittest.mock import Mock, patch

from conjector.config_handler import ConfigHandler


def patch_config(return_values: Dict[str, Any]):
    from conjector.config_handler import ConfigHandler

    return patch.object(
        ConfigHandler, "get_config", Mock(return_value=return_values)
    )


@pytest.fixture(autouse=True)
def clear_config_handler_cache():
    ConfigHandler.clear_cache()
