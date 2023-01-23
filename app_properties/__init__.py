import warnings

from .main import Conjector, properties

warnings.warn(
    "The folder name 'app_properties' is deprecated! "
    "It'll be renamed to 'conjector' in future releases.",
    DeprecationWarning,
)
__all__ = ("properties", "Conjector")
__version__ = "1.5.0"
