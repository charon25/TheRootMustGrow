from random import randint, random, choice

import pygame as pyg
import pyghelper

from tile import Tile, TileType
import constants as co


class TerrainGenerator:
    def __init__(self) -> None:
        self.depth: int = 0

    def generate_tile(self):
        tile_type = choice([TileType.BASE, TileType.BASE2] * 10 + list(TileType))
        tile = Tile(tile_type)
        if tile.is_resource_tile():
            tile.resources = 100 # TODO update
        return tile

    def starting_terrain(self) -> list[list[Tile]]:
        self.depth = -1
        terrain: list[list[Tile]] = []
        for y in range(co.TILES_Y):
            terrain.append(next(self))            

        return terrain


    def __next__(self) -> list[Tile]:
        self.depth += 1
        return [self.generate_tile() for x in range(co.TILES_X)]
