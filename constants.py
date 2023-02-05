from enum import Enum


TILE = 25
TILES_X = 32
TILES_Y = 32

WIDTH = TILES_X * TILE
HEIGHT = TILES_Y * TILE


STARTING_SCROLL_OFFSET = 5
MAX_VISIBLE_TILES_OFFSET = 18


# Roots
ROOT_HEIGHTS: dict[int, int] = {
    1: 10,
    2: 15,
    3: 20,
    4: 25
}
ROOT_END_LENGTH: dict[int, int] = {
    1: 10,
    2: 15,
    3: 20,
    4: 25
}
MAX_ROOT_WIDTH = max(ROOT_HEIGHTS.keys())
MAX_ROOT_LENGTH = 350

STARTING_DECAY_COOLDOWN = 300
MIN_DECAY_COOLDOWN = 30
MIN_DECAY_COOLDOWN_RESOURCE = -300

# Clicks
LEFT_CLICK = 1
RIGHT_CLICK = 3
MOUSE_WHEEL = 5

# Ressources
class ResourceType(Enum):
    WATER = 10
    NITROGEN = 11
    PHOSPHORUS = 12

RESOURCE_TEXT_NAME: dict[ResourceType, str] = {
    ResourceType.WATER: 'Water',
    ResourceType.NITROGEN: 'Nitrogen',
    ResourceType.PHOSPHORUS: 'Phosphorus'
}
RESOURCE_SPACES: dict[ResourceType, str] = {
    ResourceType.WATER: '     ',
    ResourceType.NITROGEN: '  ',
    ResourceType.PHOSPHORUS: ''
}

# relative / frame
STARTING_ABSORPTION_RATE: dict[ResourceType, float] = {
    ResourceType.WATER: 1 / 50,
    ResourceType.NITROGEN: 0.2 / 50,
    ResourceType.PHOSPHORUS: 0.2 / 50
}
# / frame / racine
STARTING_CONSUMPTION_RATE: dict[ResourceType, float] = {
    ResourceType.WATER: 0.00000001,
    ResourceType.NITROGEN: 0.000000001,
    ResourceType.PHOSPHORUS: 0.000000001
}


# Police
FONT_PATH = 'resources/font/monogramextended.otf'
RESOURCE_FONT_COLOR: dict[ResourceType, tuple[int, int, int]] = {
    ResourceType.WATER: (0, 0, 0),
    ResourceType.NITROGEN: (255, 255, 255),
    ResourceType.PHOSPHORUS: (255, 255, 255)
}

# UI
UI_HEIGHT = 5

UI_TOP = HEIGHT - UI_HEIGHT * TILE

RESOURCE_TEXT_COORDS: dict[ResourceType, tuple[int, int]] = {
    ResourceType.WATER: (35, 25),
    ResourceType.NITROGEN: (35, 60),
    ResourceType.PHOSPHORUS: (35, 95)
}

TOTAL_ROOTS_TEXT_COORD = (5, -4)

FPS_COORDS = (740, 100)
DEPTH_COORDS = (5, UI_TOP - 30)

# Shake
SCREENSHAKE_COUNT = 5
SCREENSHAKE_LENGTH_MAX = 200
SCREENSHAKE_AMOUNT_MAX = 4

# Particles
PARTICLE_DURATION = 30
EXTRACT_PARTICLE_PROBABILITY = 0.75
EXTRACT_PARTICLE_RADIUS = TILE / 3
EXTRACT_PARTICLE_SPEED = 0.5

# Génération terrain
FIRST_RESOURCE_LAYER_QUANTITY = (83, 83)

LEVELS_BASE_RESOURCE_PROBABILITY: list[float] = [None, # parce que les level sont indexés à 1
    0.05,
    0.05,
    0.09
]

LEVELS_RESOURCE_PROBABILITY_INCREASE: list[float] = [None, # parce que les level sont indexés à 1
    0.06,
    0.035,
    0.028
]

LEVELS_ROCK_PROBABILITY: list[float] = [None, # parce que les level sont indexés à 1
    1 / 135,
    1 / 110,
    1 / 90
]

## LEVEL 1
LEVEL_1_RESOURCES_QUANTITY = (300, 420)
LEVEL_1_DEPTH = 65
LEVEL_1_PATTERN_COUNT = 6
LEVEL_1_HEIGHT = LEVEL_1_DEPTH - (TILES_Y + 2)

## LEVEL 2
LEVEL_2_RESOURCES_QUANTITY = (700, 950)
LEVEL_2_DEPTH = 170
LEVEL_2_PATTERN_COUNT = 9
LEVEL_2_HEIGHT = LEVEL_2_DEPTH - LEVEL_1_DEPTH

## LEVEL 2
LEVEL_3_RESOURCES_QUANTITY = (1000, 1300)
LEVEL_3_DEPTH = 300
LEVEL_3_PATTERN_COUNT = 15
LEVEL_3_HEIGHT = LEVEL_3_DEPTH - LEVEL_2_DEPTH
