from random import randint, random, choice

import pygame as pyg
import pyghelper

import constants as co
import textures as tx
from tile import Tile, TileType


class TerrainGenerator:
    def __init__(self) -> None:
        self.depth: int = 0

    def generate_tile(self, x: int, y: int):
        tile_type = choice([TileType.BASE] * 10 + list(TileType))
        tile = Tile(tile_type, x, y)

        if tile.is_resource_tile():
            tile.resource = 100 # TODO update

        if tile.type == TileType.BASE:
            tile.texture = choice(tx.BASE_TILES)
        return tile

    def starting_terrain(self) -> list[list[Tile]]:
        self.depth = -1
        terrain: list[list[Tile]] = []
        for y in range(co.TILES_Y):
            terrain.append(next(self))

        return terrain


    def __next__(self) -> list[Tile]:
        self.depth += 1
        return [self.generate_tile(x, self.depth) for x in range(co.TILES_X)]
