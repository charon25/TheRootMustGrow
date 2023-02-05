import random

import constants as co

BASE_PATTERN = ['x']

PATTERN1 = ([' r', ' r', 'xr', ' r', ' r'], (0, co.TILES_X / 3))
PATTERN2 = (['r ', 'r ', 'rx', 'r ', 'r '], (co.TILES_X * 2 / 3, co.TILES_X))
PATTERN8 = (['xs'], (0, co.TILES_X + 1))

LEVEL_1 = [PATTERN1, PATTERN2, PATTERN8]

PATTERN3 = (['rr', 'xr', ' r'], (0, co.TILES_X * 0.45))
PATTERN4 = (['rr', 'rx', 'r '], (co.TILES_X * 0.55, co.TILES_X))
PATTERN5 = ([' x', 's '], (0, co.TILES_X + 1))
PATTERN6 = (['x ', ' s'], (0, co.TILES_X + 1))
PATTERN7 = ([' xs', 'sxs', ' x '], (5, co.TILES_X - 5))
PATTERN9 = (['rxr', 'xrx'], (0, co.TILES_X + 1))

LEVEL_2 = [PATTERN3, PATTERN3] * 3 + [PATTERN5, PATTERN6] * 2 + [PATTERN7, PATTERN9]

PATTERN10 = (['rr', 'rx', 'rr', 'xr', 'rr'], (0, co.TILES_X + 1))
PATTERN11 = (['r r', 'r r', 'r r', 'r r', 'rxr', 'rrr'], (0, co.TILES_X + 1))
PATTERN12 = (['x x', ' r ', 's s'], (0, co.TILES_X + 1))
PATTERN13 = (['xs', 'ss'], (0, co.TILES_X + 1))

LEVEL_3 = ([PATTERN1, PATTERN2, PATTERN3, PATTERN4] + [PATTERN10, PATTERN12, PATTERN13]) * 2 + [PATTERN11]


def get_pattern(pattern_list: list[tuple[str, tuple[float, float]]], x: int, y: int) -> list[str]:
    possible_patterns = [pattern for (pattern, (min_x, max_x)) in pattern_list if min_x <= x <= max_x]

    if not possible_patterns:
        return BASE_PATTERN

    return random.choice(possible_patterns)
