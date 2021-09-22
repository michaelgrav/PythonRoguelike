from enum import auto, Enum


# Auto assigns incrementing integer values automatically
class RenderOrder(Enum):
    """
    Assign a value to each Entity, and this value will represent which order the entities should be
    rendered in. Lower values will be rendered first, and higher values will be rendered after. Therefore,
    if we assign a low value to a corpse, it will get drawn before an entity. If two things are on the same tile,
    whatever gets drawn last will be what the player sees.
    """
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
