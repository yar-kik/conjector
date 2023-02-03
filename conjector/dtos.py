from typing import Any

from dataclasses import dataclass, fields

DEFAULT: Any = object()


@dataclass
class Settings:
    filename: str = "application.yml"
    override_default: bool = False
    root: str = ""
    type_cast: bool = True
    lazy_init: bool = False

    def __or__(self, other: "Settings") -> "Settings":
        merged_kwargs = {}
        for field in fields(Settings):
            other_val = getattr(other, field.name)
            self_val = getattr(self, field.name)
            merged_kwargs[field.name] = (
                other_val if other_val is not DEFAULT else self_val
            )
        return Settings(**merged_kwargs)
