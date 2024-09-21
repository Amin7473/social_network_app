import enum

class EnumChoices(enum.Enum):
    """Base Enum Choice class"""

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
