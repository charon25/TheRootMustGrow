from enum import Enum

from pygame import Surface
from root import Root

import constants as co
import textures as tx


class TileType(Enum):
    BASE = 0
    BASE2 = 1

    WATER = co.ResourceType.WATER.value
    NITROGEN = co.ResourceType.NITROGEN.value
    PHOSPORUS = co.ResourceType.PHOSPORUS.value


class Tile:
    def __init__(self, type: TileType) -> None:
        self.type = type
        self.has_root = False
        self.root: Root = None
        self.resources: int = -1

    def get_texture(self) -> Surface:
        # if self.has_root:
        #     return tx.ROOT_TILE
        if self.type == TileType.BASE:
            return tx.BASE_TILE
        elif self.type == TileType.BASE2:
            return tx.BASE_TILE_2
        elif self.type == TileType.WATER:
            return tx.WATER_TILE
        elif self.type == TileType.NITROGEN:
            return tx.NITROGEN_TILE
        elif self.type == TileType.PHOSPORUS:
            return tx.PHOSPORUS_TILE

    def is_resource_tile(self):
        return self.type.value // 10 == 1
