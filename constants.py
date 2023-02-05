from enum import Enum


TILE = 25
TILES_X = 32
TILES_Y = 32

WIDTH = TILES_X * TILE
HEIGHT = TILES_Y * TILE


STARTING_SCROLL_OFFSET = 5
MAX_VISIBLE_TILES_OFFSET = 18

# Game State
class GameState(Enum):
    MENU = 0
    TUTORIAL = 1
    GAME = 2

# Menu

PLAY_BTN_X, PLAY_BTN_Y = (150, 384)
TUTO_BTN_X, TUTO_BTN_Y = (150, 510)
QUIT_BTN_X, QUIT_BTN_Y = (150, 636)
BTN_WIDTH, BTN_HEIGHT = (500, 90)


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

STARTING_DECAY_COOLDOWN = 500
MIN_DECAY_COOLDOWN = 90
MIN_DECAY_COOLDOWN_RESOURCE = -450

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

RESOURCES_START: dict[ResourceType, int] = {
    ResourceType.WATER: 150,
    ResourceType.NITROGEN: 200,
    ResourceType.PHOSPHORUS: 250,
}

# relative / frame
STARTING_ABSORPTION_RATE: dict[ResourceType, float] = {
    ResourceType.WATER: (1 / 20) / 60,
    ResourceType.NITROGEN: (1 / 38) / 60,
    ResourceType.PHOSPHORUS: (1 / 45) / 60
}
# / frame / racine
STARTING_CONSUMPTION_RATE: dict[ResourceType, float] = {
    ResourceType.WATER: 250 / 60 / 30 / 300 / 4,
    ResourceType.NITROGEN: 125 / 60 / 30 / 300 / 4,
    ResourceType.PHOSPHORUS: 100 / 60 / 30 / 300 / 4
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

UI_RESOURCE_TEXTURE_COORDS: dict[ResourceType, tuple[int, int]] = {
    ResourceType.WATER: (5 + 133, UI_TOP + 25 + 13),
    ResourceType.NITROGEN: (5 + 133, UI_TOP + 60 + 13),
    ResourceType.PHOSPHORUS: (5 + 133, UI_TOP + 95 + 13)
}

TOTAL_ROOTS_TEXT_COORD = (5, -4)

BONUS_TEXT_COORD = (455, -4)
PRODUCTION_BONUS_TEXT_COORD = (483, 30)
CONSUMPTION_BONUS_TEXT_COORD = (483, 65)

FPS_COORDS = (760, 110)
MEMORY_COORDS = (747, 100)
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

GAINED_RESOURCE_PARTICLE_MIN_PROBABILITY = 1 / 15
GAINED_RESOURCE_PARTICLE_MAX_PROBABILITY = 1
GAINED_RESOURCE_PARTICLE_MAX_PROBABILITY_AMOUNT = 100 / 60

BONUS_PARTICLE_RADIUS = TILE / 3
BONUS_PARTICLE_SPEED = 0.5
BONUS_PARTICLES_COUNT = 50


# Génération terrain
FIRST_RESOURCE_LAYER_QUANTITY = (50, 150)

RESOURCE_ABSORPTION_MODIFIER_MIN = 0.9
RESOURCE_ABSORPTION_MODIFIER_MAX_MIN = 1.1
RESOURCE_ABSORPTION_MODIFIER_MAX_MAX = 2
RESOURCE_ABSORPTION_MODIFIER_MAX_MAX_DEPTH = 500

BASE_BONUS_PROBABILITY = 0
BONUS_PROBABILITY_INC = 0.01

## LEVELS
LEVELS_BASE_RESOURCE_PROBABILITY: list[float] = [None, # parce que les level sont indexés à 1
    0.05,
    0.05,
    0.09,
    0.15,
    0.2
]

LEVELS_RESOURCE_PROBABILITY_INCREASE: list[float] = [None, # parce que les level sont indexés à 1
    0.06,
    0.035,
    0.028,
    0.10,
    0.2
]

LEVELS_ROCK_PROBABILITY: list[float] = [None, # parce que les level sont indexés à 1
    1 / 135,
    1 / 110,
    1 / 90,
    1 / 75
]

## LEVEL 1
LEVEL_1_RESOURCES_QUANTITY = (300, 420)
LEVEL_1_DEPTH = 55
LEVEL_1_PATTERN_COUNT = 6
LEVEL_1_HEIGHT = LEVEL_1_DEPTH - (TILES_Y + 2)

## LEVEL 2
LEVEL_2_RESOURCES_QUANTITY = (700, 950)
LEVEL_2_DEPTH = 130
LEVEL_2_PATTERN_COUNT = 9
LEVEL_2_HEIGHT = LEVEL_2_DEPTH - LEVEL_1_DEPTH

## LEVEL 3
LEVEL_3_RESOURCES_QUANTITY = (1000, 1300)
LEVEL_3_DEPTH = 250
LEVEL_3_PATTERN_COUNT = 15
LEVEL_3_HEIGHT = LEVEL_3_DEPTH - LEVEL_2_DEPTH

## LEVEL 4
LEVEL_4_RESOURCES_QUANTITY = (2200, 2700)
LEVEL_4_DEPTH = 550
LEVEL_4_PATTERN_COUNT = 35
LEVEL_4_HEIGHT = LEVEL_4_DEPTH - LEVEL_3_DEPTH

## END
END_HEIGHT = LEVEL_4_DEPTH + 1
END_RESOURCE_START = 3500
END_RESOURCE_SCALING_ADD = 50 # / tile
END_RESOURCE_SCALING_MULT = 1.001 # / tile
END_RESOURCE_VARIANCE = 1.1
def get_end_resource_quantities(depth: int) -> tuple[int, int]:
    depth = depth - END_HEIGHT
    base = (END_RESOURCE_START + END_RESOURCE_SCALING_ADD * depth) * (END_RESOURCE_SCALING_MULT ** depth)
    return (int(base), int(base * END_RESOURCE_VARIANCE))

END_ROCK_INV_PROBABILITY_START = 70
END_ROCK_INV_PROBABILITY_MAX = 8
_a = (END_ROCK_INV_PROBABILITY_START - END_ROCK_INV_PROBABILITY_MAX) * (END_HEIGHT ** 4)
def get_end_rock_probability(depth: int):
    return 1 / (END_ROCK_INV_PROBABILITY_MAX + _a / (depth ** 4))

END_PATTERN_STARTING_GAP = 10
END_PATTERN_END_GAP = 3

END_PATTERN_END_GAP_DEPTH = 150

# Bonus

class BonusType(Enum):
    PRODUCTION = 20
    CONSUMPTION = 21

BONUS_SCREENSHAKE = 8

## Production
PRODUCTION_BONUS_BASE = 0.03
PRODUCTION_BONUS_INC = 0.0003 # / tile
PRODUCTION_BONUS_VARIANCE = 0.1

## Consommation
CONSUMPTION_BONUS_BASE = -0.015
CONSUMPTION_BONUS_INC = -0.0001 # / tile
CONSUMPTION_BONUS_VARIANCE = 0.1

RESOURCE_TO_BONUS_PROBABILITY = 0.1

# Tutoriel
TUTORIAL_MAX_LEVEL = 4

TUTORIAL_TEXTS = [None,
    [
        "Tutorial",
        "Click on a existing root (===>)", "then on the ground", "to create a new root.", "",
        "Connect a root to resources", "to harvest them.", "", "", "", "", "", "",
        "But beware! The more roots, the faster you lose resources!", "",
        "You can delete an end root by right clicking it", "",
        "Get all the resources from the screen to go to the next screen.", ""
        # "Go deeper and deeper to get more resources.", "",
        "The root must GROW!"
    ],
    [
        "The map is vertically infinite!", "",
        "To scroll, use the mouse wheel", "or drag the screen with left click", "", "",
        "You are only limited by your current longest root.", "",
        "By the way, the root you place is limited in length.", 
        "So you need to split it up to go deeper."
    ],
    [
        "You can also find bonuses on the way.", "", "",
        "They provide permanent upgrade for resource management.", "", "",
        "By the way, roots cannot cross each other."
    ]
]

TUTORIAL_TEXT_X = 5
TUTORIAL_TEXT_Y_START = 20

# Sons

MUSIC = 'music'
MUSIC_PATH= ''

SOUND_CLICK = 'click'
SOUND_CLICK_PATH = 'resources/audio/sounds/simple_click.wav'

SOUND_ROOT_GROW = 'root_grow'
SOUND_ROOT_GROW_PATHS = [f'resources/audio/sounds/root_grow_{i}.wav' for i in (1, 2, 3)]

SOUND_ROOT_CUT = 'root_cut'
SOUND_ROOT_CUT_PATHS = [f'resources/audio/sounds/root_cut_{i}.wav' for i in (1, 2, 3)]

SOUND_ROOT_DIE = 'root_die'
SOUND_ROOT_DIE_PATHS = [f'resources/audio/sounds/root_die_{i}.wav' for i in (1, 2)]

SOUND_WATER = 'water'
SOUND_WATER_PATHS = [f'resources/audio/sounds/water_{i}.wav' for i in (1, 2)]

SOUND_RESOURCE = 'resource'
SOUND_RESOURCE_PATHS = [f'resources/audio/sounds/resource_{i}.wav' for i in (1, 2)]

SOUND_BONUS = 'bonus'
SOUND_BONUS_PATH = 'resources/audio/sounds/bonus.wav'

SOUND_TUTO_PAGE = 'tuto_page'
SOUND_TUTO_PAGE_PATH = 'resources/audio/sounds/tuto_page.wav'

SOUND_TUTO_END = 'tuto_end'
SOUND_TUTO_END_PATH = 'resources/audio/sounds/tuto_end.wav'

SOUND_LOSE = 'lose'
SOUND_LOSE_PATH = 'resources/audio/sounds/lose.wav'

SOUND_WARNING = 'warning'
SOUND_WARNING_PATH = 'resources/audio/sounds/warning.wav'
