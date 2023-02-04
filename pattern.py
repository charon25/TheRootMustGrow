import random

import constants as co

BASE_PATTERN = (['x', (0, co.TILES_X)])

PATTERN1 = ([' r', ' r', 'xr', ' r', ' r'], (0, co.TILES_X // 3))
PATTERN2 = (['r ', 'r ', 'rx', 'r ', 'r '], ((co.TILES_X * 2) // 3, co.TILES_X))

LEVEL1 = [PATTERN1, PATTERN2]

def get_level_1_pattern(x: int, y: int) -> list[str]:
    possible_patterns = [pattern for (pattern, (min_x, max_x)) in LEVEL1 if min_x <= x <= max_x]
    if not possible_patterns:
        return BASE_PATTERN[0]
    return random.choice(possible_patterns)
