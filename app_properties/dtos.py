from dataclasses import dataclass, fields


@dataclass
class Settings:
    filename: str = "application.yml"
    ignore_case: bool = True
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
                other_val if other_val != field.default else self_val
            )
        return Settings(**merged_kwargs)
