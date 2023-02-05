
import pygame
import pyghelper

UI_BACKGROUND = pyghelper.Image.create('resources/textures/ui_background.png')

# TILES
BASE_TILE_TEXTURES_COUNT = 3
BASE_TILES = [pyghelper.Image.create(f'resources/textures/tiles/base_{i}.png') for i in range(1, BASE_TILE_TEXTURES_COUNT + 1)]

EMPTY_TILE = pyghelper.Image.create('resources/textures/tiles/empty.png')

WATER_TILE_TEXTURES_COUNT = 3
WATER_TILES = [pyghelper.Image.create(f'resources/textures/tiles/water_{i}.png') for i in range(1, WATER_TILE_TEXTURES_COUNT + 1)]

NITROGEN_TILE_TEXTURES_COUNT = 3
NITROGEN_TILES = [pyghelper.Image.create(f'resources/textures/tiles/nitrogen_{i}.png') for i in range(1, NITROGEN_TILE_TEXTURES_COUNT + 1)]

PHOSPHORUS_TILE_TEXTURES_COUNT = 3
PHOSPHORUS_TILES = [pyghelper.Image.create(f'resources/textures/tiles/phosphorus_{i}.png') for i in range(1, WATER_TILE_TEXTURES_COUNT + 1)]

ROCK_TILE_TEXTURES_COUNT = 2
ROCK_TILES = [pyghelper.Image.create(f'resources/textures/tiles/rock_{i}.png') for i in range(1, ROCK_TILE_TEXTURES_COUNT + 1)]


# ROOTS
ROOTS: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/root_w{i}.png') for i in (1, 2, 3, 4)}
RED_ROOTS: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/root_red_w1.png') for i in (1, 2, 3, 4)}
OVER_ROOTS: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/root_over_w{i}.png') for i in (1, 2, 3, 4)}
ROOTS_END: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/end_w{i}.png') for i in (1, 2, 3, 4)}
RED_ROOTS_END: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/end_red_w1.png') for i in (1, 2, 3, 4)}
OVER_ROOTS_END: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/end_over_w{i}.png') for i in (1, 2, 3, 4)}

# PARTICLES

WATER_PARTICLES_COUNT = 2
WATER_PARTICLES = [pyghelper.Image.create(f'resources/textures/particles/water_{i}.png') for i in range(1, WATER_PARTICLES_COUNT + 1)]

NITROGEN_PARTICLES_COUNT = 3
NITROGEN_PARTICLES = [pyghelper.Image.create(f'resources/textures/particles/nitrogen_{i}.png') for i in range(1, NITROGEN_PARTICLES_COUNT + 1)]

PHOSPHORUS_PARTICLES_COUNT = 3
PHOSPHORUS_PARTICLES = [pyghelper.Image.create(f'resources/textures/particles/phosphorus_{i}.png') for i in range(1, PHOSPHORUS_PARTICLES_COUNT + 1)]
