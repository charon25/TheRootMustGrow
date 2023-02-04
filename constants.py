from enum import Enum


TILE = 25
TILES_X = 32
TILES_Y = 32

WIDTH = TILES_X * TILE
HEIGHT = TILES_Y * TILE


STARTING_SCROLL_OFFSET = 5
MAX_VISIBLE_TILES_OFFSET = 18


# Roots
GHOST_ROOT_HEIGHT = 10
MAX_ROOT_LENGTH = 350

STARTING_DECAY_COOLDOWN = 350

# Clicks
LEFT_CLICK = 1
RIGHT_CLICK = 3
MOUSE_WHEEL = 5

# Ressources
class ResourceType(Enum):
    WATER = 10
    NITROGEN = 11
    PHOSPHORUS = 12

STARTING_ABSORPTION_RATE: dict[ResourceType, float] = {
    ResourceType.WATER: 1,
    ResourceType.NITROGEN: 0.2,
    ResourceType.PHOSPHORUS: 0.2
}
STARTING_CONSUMPTION_RATE: dict[ResourceType, float] = {
    ResourceType.WATER: 0,#.001,
    ResourceType.NITROGEN: 0,#.0001,
    ResourceType.PHOSPHORUS: 0#,.0001
}


# Police

FONT_PATH = 'resources/font/16bfZX.ttf'
RESOURCE_FONT_COLOR: dict[ResourceType, tuple[int, int, int]] = {
    ResourceType.WATER: (0, 0, 0),
    ResourceType.NITROGEN: (255, 255, 255),
    ResourceType.PHOSPHORUS: (0, 0, 0)
}
