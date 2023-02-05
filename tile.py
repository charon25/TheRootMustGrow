from enum import Enum
from random import choice

from pygame import Surface
from root import Root

import constants as co
import textures as tx


class TileType(Enum):
    BASE = 0

    ROCK = 5

    WATER = co.ResourceType.WATER.value
    NITROGEN = co.ResourceType.NITROGEN.value
    PHOSPHORUS = co.ResourceType.PHOSPHORUS.value


def get_random_texture(tile_type: TileType) -> Surface:
    if tile_type == TileType.ROCK:
        return choice(tx.ROCK_TILES)

    if tile_type == TileType.WATER:
        return choice(tx.WATER_TILES)

    if tile_type == TileType.NITROGEN:
        return choice(tx.NITROGEN_TILES)

    if tile_type == TileType.PHOSPHORUS:
        return choice(tx.PHOSPHORUS_TILES)


class Tile:
    def __init__(self, type: TileType, x: int, y: int) -> None:
        self.type = type
        self.has_root = False
        self.root: Root = None
        self.resource: int = -1
        self.x = x
        self.y = y
        self.texture: Surface = choice(tx.BASE_TILES)
        self.resource_textures: Surface = get_random_texture(self.type)

    def get_texture(self) -> Surface:
        if self.is_resource_tile():
            if self.resource > 0:
                return self.texture
            else:
                return tx.EMPTY_TILE

        return self.texture

    def is_resource_tile(self):
        return self.type.value // 10 == 1

    def get_resource_type(self):
        return co.ResourceType(self.type.value)

    def __repr__(self) -> str:
        return f'{self.type.name} : {self.x} / {self.y}'
