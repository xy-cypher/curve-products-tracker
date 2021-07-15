# borrowed from https://stackoverflow.com/a/58081120
from dataclasses import fields
from typing import Any

from marshmallow_dataclass import dataclass


@dataclass
class DefaultVal:
    val: Any


@dataclass
class NoneRefersDefault:
    def __post_init__(self):
        """If a field of this data class defines a default value of type
        `DefaultVal`, then use its value in case the field after initialization
        has either not changed or is None.
        """
        for field in fields(self):
            if isinstance(field.default, DefaultVal):
                field_val = getattr(self, field.name)
                if isinstance(field_val, DefaultVal) or field_val is None:
                    setattr(self, field.name, field.default.val)
