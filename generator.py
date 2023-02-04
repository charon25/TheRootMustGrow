from random import randint, randrange, random, choice, shuffle

import pygame as pyg
import pyghelper

import constants as co
import pattern as pat
import textures as tx
from tile import Tile, TileType


class TerrainGenerator:
    def __init__(self) -> None:
        self.depth: int = 0
        # Pattern
        self.in_pattern: list[int] = list()
        self.patterns: list[str] = list()
        self.pattern_x: list[int] = list()
        self.pattern_depths: list[int] = list()
        self.patterns_offset: list[int] = list()
        # Ressources
        self.current_resource_probability: float = 0

    def generate_tile(self, x: int, y: int):
        tile = Tile(TileType.BASE, x, y)

        if tile.is_resource_tile():
            tile.resource = 100 # TODO update

        if tile.type == TileType.BASE:
            tile.texture = choice(tx.BASE_TILES)
        return tile

    def _equitable_resource(self, cycle: int = 1):
        while True:
            resources = list(co.ResourceType) * cycle
            shuffle(resources)
            yield from [TileType(resource.value) for resource in resources]

    def _resources_quantities(self, min: int, max: int):
        while True:
            yield randint(min, max)

    def _get_pattern_tiles(self, pattern_str: str, x: int, y: int) -> list[Tile]:
        pattern: list[Tile] = []
        for dx, c in enumerate(pattern_str):
            if c == 'r':
                tile = Tile(TileType.ROCK, x + dx, y)
            elif c == 'x':
                tile = Tile(next(self.terrain_resources), x + dx, y)
                tile.resource = next(self.resources_quantities)
            else:
                tile = Tile(TileType.BASE, x + dx, y)

            pattern.append(tile)

        return pattern


    def _generate_first_resource_layer(self) -> list[Tile]:
        if self.depth % 2 == 1:
            resource_x = randrange(5, co.TILES_X - 5)
            resource_type = next(self.terrain_resources)
        else:
            resource_x = -1

        row = []
        for x in range(co.TILES_X):
            if x == resource_x:
                tile = Tile(resource_type, x, self.depth)
                tile.resource = randint(*co.FIRST_RESOURCE_LAYER_QUANTITY)
                row.append(tile)
            else:
                row.append(Tile(TileType.BASE, x, self.depth))

        return row

    def _generate_second_resource_layer(self) -> list[Tile]:
        if self.depth % 4 == 1:
            special_x = randrange(0, co.TILES_X)
            resource_type = next(self.terrain_resources)
        elif self.depth % 4 == 3:
            special_x = randrange(10, co.TILES_X - 10)
            resource_type = TileType.ROCK
        else:
            special_x = -1

        row = []
        for x in range(co.TILES_X):
            if x == special_x:
                tile = Tile(resource_type, x, self.depth)
                if tile.is_resource_tile():
                    tile.resource = randint(*co.FIRST_RESOURCE_LAYER_QUANTITY)
                row.append(tile)
            else:
                row.append(Tile(TileType.BASE, x, self.depth))

        return row

    def _generate_levels_layer(self, level: int):
        if self.depth in self.pattern_depths:
            for index, depth in enumerate(self.pattern_depths):
                if depth == self.depth:
                    self.in_pattern.append(index)

        row: list[Tile] = [None] * co.TILES_X

        for index in self.in_pattern:
            if self.patterns_offset[index] >= len(self.patterns[index]):
                self.in_pattern.remove(index)
                break

            pattern_tiles = self._get_pattern_tiles(self.patterns[index][self.patterns_offset[index]], self.pattern_x[index], self.pattern_depths[index] + self.patterns_offset[index])
            row[self.pattern_x[index]:self.pattern_x[index]+len(self.patterns[index][0])] = pattern_tiles

            self.patterns_offset[index] += 1

        row = [Tile(TileType.BASE, x, self.depth) if tile is None else tile for x, tile in enumerate(row)]

        if random() < self.current_resource_probability:
            resource_x = randrange(0, co.TILES_X)
            resource_type = next(self.terrain_resources)
            row[resource_x] = Tile(resource_type, resource_x, self.depth)
            row[resource_x].resource = next(self.resources_quantities)
            self.current_resource_probability = co.LEVELS_BASE_RESOURCE_PROBABILITY[level]
        else:
            self.current_resource_probability += co.LEVELS_RESOURCE_PROBABILITY_INCREASE[level]

        return row[:co.TILES_X]

    def _setup_level_1(self):
        self.terrain_resources = self._equitable_resource(2)
        self.resources_quantities = self._resources_quantities(*co.LEVEL_1_RESOURCES_QUANTITY)

        self.in_pattern = []
        self.pattern_x = [randint(0, co.TILES_X) - 2 for index in range(co.LEVEL_1_PATTERN_COUNT)]
        self.pattern_depths = [randint(self.depth, co.LEVEL_1_DEPTH) for _ in range(co.LEVEL_1_PATTERN_COUNT)]
        self.patterns = [pat.get_pattern(pat.LEVEL_1, self.pattern_x[index], self.pattern_depths[index]) for index in range(co.LEVEL_1_PATTERN_COUNT)]
        self.patterns_offset = [0] * co.LEVEL_1_PATTERN_COUNT

        self.current_resource_probability = co.LEVELS_BASE_RESOURCE_PROBABILITY[1]

    def _setup_level_2(self):
        self.terrain_resources = self._equitable_resource(2)
        self.resources_quantities = self._resources_quantities(*co.LEVEL_2_RESOURCES_QUANTITY)

        self.in_pattern = []
        self.pattern_x = [randint(0, co.TILES_X) - 2 for index in range(co.LEVEL_2_PATTERN_COUNT)]
        self.pattern_depths = [randint(self.depth, co.LEVEL_2_DEPTH) for _ in range(co.LEVEL_2_PATTERN_COUNT)]
        self.patterns = [pat.get_pattern(pat.LEVEL_2, self.pattern_x[index], self.pattern_depths[index]) for index in range(co.LEVEL_2_PATTERN_COUNT)]
        self.patterns_offset = [0] * co.LEVEL_2_PATTERN_COUNT

        self.current_resource_probability = co.LEVELS_BASE_RESOURCE_PROBABILITY[2]


    def __next__(self) -> list[Tile]:
        self.depth += 1
        if self.depth == 0:
            self.terrain_resources = self._equitable_resource(1)
            self.resources_quantities = self._resources_quantities(*co.FIRST_RESOURCE_LAYER_QUANTITY)

        if self.depth <= 4:
            return [Tile(TileType.BASE, x, self.depth) for x in range(co.TILES_X)]

        if self.depth <= 20:
            return self._generate_first_resource_layer()

        if self.depth <= co.TILES_Y + 2:
            return self._generate_second_resource_layer()

        if self.depth == co.TILES_Y + 2 + 1:
            self._setup_level_1()

        if self.depth <= co.LEVEL_1_DEPTH:
            return self._generate_levels_layer(1)

        if self.depth == co.LEVEL_1_DEPTH + 1:
            self._setup_level_2()

        if self.depth <= co.LEVEL_2_DEPTH:
            return self._generate_levels_layer(2)

        return [self.generate_tile(x, self.depth) for x in range(co.TILES_X)]

    def starting_terrain(self) -> list[list[Tile]]:
        self.depth = -1
        terrain: list[list[Tile]] = []
        for y in range(co.TILES_Y):
            terrain.append(next(self))

        return terrain
