from random import randint, randrange, random, choice, shuffle

import pygame as pyg
import pyghelper

import constants as co
import pattern as pat
import textures as tx
from tile import Tile, TileType
import utils


def generate_random_depths(count: int, start_y: int, height: int) -> list[int]:
    gap = height // count
    return [start_y + gap * i + randint(0, gap) for i in range(count)]

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
        self.last_resource_type: TileType = TileType.WATER
        # Bonus
        self.first_bonus_layer: int = -1
        self.current_bonus_probability: float = 0


    def _equitable_resource(self, cycle: int = 1):
        while True:
            resources = [co.ResourceType.WATER, co.ResourceType.WATER, co.ResourceType.NITROGEN, co.ResourceType.PHOSPHORUS] * cycle
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
                if random() < co.RESOURCE_TO_BONUS_PROBABILITY:
                    bonus_type = TileType(choice(list(co.BonusType)).value)
                    tile = Tile(bonus_type, x + dx, self.depth)
                else:
                    tile = Tile(next(self.terrain_resources), x + dx, y)
                    tile.set_starting_resource(next(self.resources_quantities), utils.random_float(co.RESOURCE_ABSORPTION_MODIFIER_MIN, utils.clamped_lerp(self.depth, 1, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MAX_DEPTH, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MIN, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MAX)))
                    self.last_resource_type = tile.type
            elif c == 's':
                if random() < co.RESOURCE_TO_BONUS_PROBABILITY:
                    bonus_type = TileType(choice(list(co.BonusType)).value)
                    tile = Tile(bonus_type, x + dx, self.depth)
                else:
                    tile = Tile(self.last_resource_type, x + dx, y)
                    tile.set_starting_resource(next(self.resources_quantities), utils.random_float(co.RESOURCE_ABSORPTION_MODIFIER_MIN, utils.clamped_lerp(self.depth, 1, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MAX_DEPTH, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MIN, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MAX)))
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
                tile.set_starting_resource(randint(*co.FIRST_RESOURCE_LAYER_QUANTITY), utils.random_float(co.RESOURCE_ABSORPTION_MODIFIER_MIN, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MIN))
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

        row: list[Tile] = []
        for x in range(co.TILES_X):
            if x == special_x:
                tile = Tile(resource_type, x, self.depth)
                if tile.is_resource_tile():
                    tile.set_starting_resource(randint(*co.FIRST_RESOURCE_LAYER_QUANTITY), utils.random_float(co.RESOURCE_ABSORPTION_MODIFIER_MIN, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MIN))
                row.append(tile)
            else:
                row.append(Tile(TileType.BASE, x, self.depth))

        if self.depth == self.first_bonus_layer:
            bonus_x = randint(8, co.TILES_X - 8)
            row[bonus_x] = Tile(choice((TileType.PRODUCTION, TileType.CONSUMPTION)), bonus_x, self.depth)
            row[bonus_x].bonus_value *= 2

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

        rock_probability = co.LEVELS_ROCK_PROBABILITY[level] if level <= 4 else co.get_end_rock_probability(self.depth)

        row = [
            (
                Tile(TileType.ROCK, x, self.depth) 
                if random() < rock_probability
                else Tile(TileType.BASE, x, self.depth)
            ) if tile is None else tile
            for x, tile in enumerate(row)
        ]

        if random() < self.current_resource_probability:
            resource_x = randrange(0, co.TILES_X)
            resource_type = next(self.terrain_resources)
            row[resource_x] = Tile(resource_type, resource_x, self.depth)
            row[resource_x].set_starting_resource(next(self.resources_quantities), utils.random_float(co.RESOURCE_ABSORPTION_MODIFIER_MIN, utils.clamped_lerp(self.depth, 1, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MAX_DEPTH, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MIN, co.RESOURCE_ABSORPTION_MODIFIER_MAX_MAX)))
            self.current_resource_probability = co.LEVELS_BASE_RESOURCE_PROBABILITY[level]
        else:
            self.current_resource_probability += co.LEVELS_RESOURCE_PROBABILITY_INCREASE[level]

        if random() < self.current_bonus_probability:
            bonus_x = randrange(1, co.TILES_X - 1)
            bonus_type = TileType(choice(list(co.BonusType)).value)
            row[bonus_x] = Tile(bonus_type, bonus_x, self.depth)
            self.current_bonus_probability = co.BASE_BONUS_PROBABILITY
        else:
            self.current_bonus_probability += co.BONUS_PROBABILITY_INC

        return row[:co.TILES_X]


    def _setup_level_1(self):
        self.terrain_resources = self._equitable_resource(2)
        self.resources_quantities = self._resources_quantities(*co.LEVEL_1_RESOURCES_QUANTITY)

        self.in_pattern = []
        self.pattern_x = [randint(0, co.TILES_X) - 2 for index in range(co.LEVEL_1_PATTERN_COUNT)]
        self.pattern_depths = generate_random_depths(co.LEVEL_1_PATTERN_COUNT, self.depth, co.LEVEL_1_HEIGHT)
        self.patterns = [pat.get_pattern(pat.LEVEL_1, self.pattern_x[index], self.pattern_depths[index]) for index in range(co.LEVEL_1_PATTERN_COUNT)]
        self.patterns_offset = [0] * co.LEVEL_1_PATTERN_COUNT

        self.current_resource_probability = co.LEVELS_BASE_RESOURCE_PROBABILITY[1]

    def _setup_level_2(self):
        self.terrain_resources = self._equitable_resource(2)
        self.resources_quantities = self._resources_quantities(*co.LEVEL_2_RESOURCES_QUANTITY)

        self.in_pattern = []
        self.pattern_x = [randint(0, co.TILES_X) - 2 for index in range(co.LEVEL_2_PATTERN_COUNT)]
        self.pattern_depths = generate_random_depths(co.LEVEL_2_PATTERN_COUNT, self.depth, co.LEVEL_2_HEIGHT)
        self.patterns = [pat.get_pattern(pat.LEVEL_2, self.pattern_x[index], self.pattern_depths[index]) for index in range(co.LEVEL_2_PATTERN_COUNT)]
        self.patterns_offset = [0] * co.LEVEL_2_PATTERN_COUNT

        self.current_resource_probability = co.LEVELS_BASE_RESOURCE_PROBABILITY[2]


    def _setup_level_3(self):
        self.terrain_resources = self._equitable_resource(2)
        self.resources_quantities = self._resources_quantities(*co.LEVEL_3_RESOURCES_QUANTITY)

        self.in_pattern = []
        self.pattern_x = [randint(0, co.TILES_X) - 2 for index in range(co.LEVEL_3_PATTERN_COUNT)]
        self.pattern_depths = generate_random_depths(co.LEVEL_3_PATTERN_COUNT, self.depth, co.LEVEL_3_HEIGHT)
        self.patterns = [pat.get_pattern(pat.LEVEL_3, self.pattern_x[index], self.pattern_depths[index]) for index in range(co.LEVEL_3_PATTERN_COUNT)]
        self.patterns_offset = [0] * co.LEVEL_3_PATTERN_COUNT

        self.current_resource_probability = co.LEVELS_BASE_RESOURCE_PROBABILITY[3]


    def _setup_level_4(self):
        self.terrain_resources = self._equitable_resource(3)
        self.resources_quantities = self._resources_quantities(*co.LEVEL_4_RESOURCES_QUANTITY)

        self.in_pattern = []
        self.pattern_x = [randint(0, co.TILES_X) - 2 for index in range(co.LEVEL_4_PATTERN_COUNT)]
        self.pattern_depths = generate_random_depths(co.LEVEL_4_PATTERN_COUNT, self.depth, co.LEVEL_4_HEIGHT)
        self.patterns = [pat.get_pattern(pat.LEVEL_4, self.pattern_x[index], self.pattern_depths[index]) for index in range(co.LEVEL_4_PATTERN_COUNT)]
        self.patterns_offset = [0] * co.LEVEL_4_PATTERN_COUNT

        self.current_resource_probability = co.LEVELS_BASE_RESOURCE_PROBABILITY[4]


    def _setup_end(self):
        self.terrain_resources = self._equitable_resource(3)
        self.patterns = []


    def __next__(self) -> list[Tile]:
        self.depth += 1
        if self.depth == 0:
            self.terrain_resources = self._equitable_resource(1)
            self.resources_quantities = self._resources_quantities(*co.FIRST_RESOURCE_LAYER_QUANTITY)

        if self.depth <= 4:
            return [Tile(TileType.BASE, x, self.depth) for x in range(co.TILES_X)]

        if self.depth <= 20:
            return self._generate_first_resource_layer()

        if self.depth == 21:
            self.first_bonus_layer = randint(21, 27)

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

        if self.depth == co.LEVEL_2_DEPTH + 1:
            self._setup_level_3()

        if self.depth <= co.LEVEL_3_DEPTH:
            return self._generate_levels_layer(3)

        if self.depth == co.LEVEL_3_DEPTH + 1:
            self._setup_level_4()

        if self.depth <= co.LEVEL_4_DEPTH:
            return self._generate_levels_layer(4)

        if self.depth == co.LEVEL_4_DEPTH + 1:
            self._setup_end()

        self.resources_quantities = self._resources_quantities(*co.get_end_resource_quantities(self.depth))

        if not self.in_pattern:
            self.in_pattern = []
            self.pattern_x = [randint(0, co.TILES_X) - 2]
            self.pattern_depths = [randint(self.depth, self.depth + int(round(utils.clamped_lerp(self.depth - co.END_HEIGHT, 0, co.END_PATTERN_END_GAP_DEPTH, co.END_PATTERN_STARTING_GAP, co.END_PATTERN_END_GAP), 0)))]
            self.patterns = [pat.get_pattern(pat.ALL_PATTERNS, self.pattern_x[0], self.pattern_depths[0])]
            self.patterns_offset = [0]

        return self._generate_levels_layer(5)

    def starting_terrain(self) -> list[list[Tile]]:
        self.depth = -1
        terrain: list[list[Tile]] = []
        for y in range(co.TILES_Y):
            terrain.append(next(self))

        return terrain

    def get_level(self, depth):
        if depth <= co.TILES_Y + 2:
            return 0

        if depth <= co.LEVEL_1_DEPTH:
            return 1

        if depth <= co.LEVEL_2_DEPTH:
            return 2

        if depth <= co.LEVEL_3_DEPTH:
            return 3

        if depth <= co.LEVEL_4_DEPTH:
            return 4

        return '*'
