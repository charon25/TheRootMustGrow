from enum import Enum

from pygame import Surface

import constants as co
import textures as tx


class TileType(Enum):
    BASE = 0
    BASE2 = 1
    ROOT = 2


class Tile:
    def __init__(self, type: TileType) -> None:
        self.type = type
        self.has_root = False

    def get_texture(self) -> Surface:
        if self.type == TileType.BASE:
            return tx.BASE_TILE
        elif self.type == TileType.BASE2:
            return tx.BASE_TILE_2
        elif self.type == TileType.ROOT:
            return tx.ROOT_TILE
