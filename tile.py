from enum import Enum
from random import choice

from pygame import Surface
from root import Root

import constants as co
import textures as tx


class TileType(Enum):
    BASE = 0

    WATER = co.ResourceType.WATER.value
    NITROGEN = co.ResourceType.NITROGEN.value
    PHOSPHORUS = co.ResourceType.PHOSPHORUS.value


def get_random_texture(tile_type: TileType) -> Surface:
    if tile_type == TileType.BASE:
        return choice(tx.BASE_TILES)
    
    if tile_type == TileType.WATER:
        return tx.WATER_TILE
    
    if tile_type == TileType.NITROGEN:
        return choice(tx.NITROGEN_TILES)

    if tile_type == TileType.PHOSPHORUS:
        return tx.PHOSPORUS_TILE


class Tile:
    def __init__(self, type: TileType, x: int, y: int) -> None:
        self.type = type
        self.has_root = False
        self.root: Root = None
        self.resource: int = -1
        self.x = x
        self.y = y
        self.texture: Surface = get_random_texture(self.type)

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
