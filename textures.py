
import pygame
import pyghelper


BACKGROUND = pyghelper.Image.create('resources/textures/background.png')
UI_BACKGROUND = pyghelper.Image.create('resources/textures/ui_background.png')

BASE_TILE = pyghelper.Image.create('resources/textures/base_tile.png')
BASE_TILE_2 = pyghelper.Image.create('resources/textures/base_tile_2.png')
ROOT_TILE = pyghelper.Image.create('resources/textures/root_tile.png')
WATER_TILE = pyghelper.Image.create('resources/textures/water.png')
NITROGEN_TILE = pyghelper.Image.create('resources/textures/nitrogen.png')
PHOSPORUS_TILE = pyghelper.Image.create('resources/textures/phosporus.png')

ROOTS: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/root_w{i}.png') for i in (1, 2, 3, 4)}
RED_ROOTS: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/root_red_w1.png') for i in (1, 2, 3, 4)}
ROOTS_END: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/end_w{i}.png') for i in (1, 2, 3, 4)}
RED_ROOTS_END: dict[int, pygame.Surface] = {i: pyghelper.Image.create(f'resources/textures/roots/end_red_w1.png') for i in (1, 2, 3, 4)}
