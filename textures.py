
import pygame
import pyghelper


BACKGROUND = pyghelper.Image.create('resources/textures/background.png')
UI_BACKGROUND = pyghelper.Image.create('resources/textures/ui_background.png')

BASE_TILE_TEXTURES_COUNT = 3
BASE_TILES = [pyghelper.Image.create(f'resources/textures/tiles/base_{i}.png') for i in range(1, BASE_TILE_TEXTURES_COUNT + 1)]

ROOT_TILE = pyghelper.Image.create('resources/textures/root_tile.png')

EMPTY_TILE = pyghelper.Image.create('resources/textures/tiles/empty.png')

WATER_TILE_TEXTURES_COUNT = 3
WATER_TILES = [pyghelper.Image.create(f'resources/textures/tiles/water_{i}.png') for i in range(1, WATER_TILE_TEXTURES_COUNT + 1)]

NITROGEN_TILE_TEXTURES_COUNT = 3
NITROGEN_TILES = [pyghelper.Image.create(f'resources/textures/tiles/nitrogen_{i}.png') for i in range(1, NITROGEN_TILE_TEXTURES_COUNT + 1)]

PHOSPHORUS_TILE_TEXTURES_COUNT = 3
PHOSPHORUS_TILES = [pyghelper.Image.create(f'resources/textures/tiles/phosphorus_{i}.png') for i in range(1, WATER_TILE_TEXTURES_COUNT + 1)]

ROOTS: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/root_w{i}.png') for i in (1, 2, 3, 4)}
RED_ROOTS: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/root_red_w1.png') for i in (1, 2, 3, 4)}
ROOTS_END: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/end_w{i}.png') for i in (1, 2, 3, 4)}
RED_ROOTS_END: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/end_red_w1.png') for i in (1, 2, 3, 4)}
