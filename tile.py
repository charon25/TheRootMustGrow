from enum import Enum
from random import choice

from pygame import Surface
from root import Root

import constants as co
import textures as tx
import utils


class TileType(Enum):
    BASE = 0

    ROCK = 5

    WATER = co.ResourceType.WATER.value
    NITROGEN = co.ResourceType.NITROGEN.value
    PHOSPHORUS = co.ResourceType.PHOSPHORUS.value

    PRODUCTION = co.BonusType.PRODUCTION.value
    CONSUMPTION = co.BonusType.CONSUMPTION.value


def get_random_texture(tile_type: TileType) -> Surface:
    if tile_type == TileType.BASE:
        return None

    if tile_type == TileType.ROCK:
        return choice(tx.ROCK_TILES)

    if tile_type == TileType.WATER:
        return choice(tx.WATER_TILES)

    if tile_type == TileType.NITROGEN:
        return choice(tx.NITROGEN_TILES)

    if tile_type == TileType.PHOSPHORUS:
        return choice(tx.PHOSPHORUS_TILES)

    return tx.BONUS_TILES[co.BonusType(tile_type.value)]


class Tile:
    def __init__(self, type: TileType, x: int, y: int) -> None:
        self.type = type
        self.has_root = False
        self.root: Root = None
        self.resource: int = -1
        self.starting_resource: int = -1
        self.x = x
        self.y = y
        self.texture: Surface = choice(tx.BASE_TILES)
        self.resource_textures: Surface = get_random_texture(self.type)
        self.absorption_modifier: float = 1.0
        self.bonus_value: float = None

        if self.is_bonus_tile():
            self.update_bonus_value()


    def update_bonus_value(self):
        if self.type == TileType.PRODUCTION:
            base = co.PRODUCTION_BONUS_BASE + self.y * co.PRODUCTION_BONUS_INC
            self.bonus_value = utils.random_float(base * (1 - co.PRODUCTION_BONUS_VARIANCE), base * (1 + co.PRODUCTION_BONUS_VARIANCE))

        elif self.type == TileType.CONSUMPTION:
            base = co.CONSUMPTION_BONUS_BASE + self.y * co.CONSUMPTION_BONUS_INC
            self.bonus_value = utils.random_float(base * (1 - co.CONSUMPTION_BONUS_VARIANCE), base * (1 + co.CONSUMPTION_BONUS_VARIANCE))


    def get_texture(self) -> Surface:
        if self.is_resource_tile():
            if self.resource > 0:
                return self.texture
            else:
                return tx.EMPTY_TILE

        return self.texture

    def is_resource_tile(self):
        return self.type.value // 10 == 1

    def is_bonus_tile(self):
        return self.type.value // 10 == 2

    def get_resource_type(self):
        return co.ResourceType(self.type.value)

    def __repr__(self) -> str:
        return f'{self.type.name} : {self.x} / {self.y}'

    def set_starting_resource(self, starting_resource: int, absorption_modifier: float):
        self.resource = starting_resource
        self.starting_resource = starting_resource
        self.absorption_modifier = absorption_modifier

    def consume(self, rate: float):
        quantity = rate * self.absorption_modifier * self.starting_resource
        if quantity < self.resource:
            self.resource -= quantity
            return quantity
        else:
            value = self.resource
            self.resource = 0
            return value
