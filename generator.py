from random import randint, random

import pygame as pyg
import pyghelper

from tile import Tile, TileType
import constants as co


class TerrainGenerator:
    def __init__(self) -> None:
        self.depth: int = 0

    def starting_terrain(self) -> list[list[Tile]]:
        self.depth = co.TILES_Y
        return [[Tile(TileType(randint(0, 1))) for x in range(co.TILES_X)] for y in range(co.TILES_Y)]

    def __next__(self) -> list[Tile]:
        self.depth += 1
        return [Tile(TileType(randint(0, 1))) for x in range(co.TILES_X)]
