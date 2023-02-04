import random

import constants as co

BASE_PATTERN = ['x']

PATTERN1 = ([' r', ' r', 'xr', ' r', ' r'], (0, co.TILES_X / 3))
PATTERN2 = (['r ', 'r ', 'rx', 'r ', 'r '], (co.TILES_X * 2 / 3, co.TILES_X))

LEVEL_1 = [PATTERN1, PATTERN2]

PATTERN3 = (['rr', 'xr', ' r'], (0, co.TILES_X * 0.45))
PATTERN4 = (['rr', 'rx', 'r '], (co.TILES_X * 0.55, co.TILES_X))

LEVEL_2 = [PATTERN3, PATTERN4]

def get_pattern(pattern_list: list[tuple[str, tuple[float, float]]], x: int, y: int) -> list[str]:
    possible_patterns = [pattern for (pattern, (min_x, max_x)) in pattern_list if min_x <= x <= max_x]

    if not possible_patterns:
        return BASE_PATTERN

    return random.choice(possible_patterns)
