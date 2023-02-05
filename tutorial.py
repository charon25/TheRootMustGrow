import constants as co
from tile import Tile, TileType


class Tutorial:
    def __init__(self) -> None:
        self.level: int = 1
        self.depth = 0

    def __next__(self):
        return [Tile(TileType.BASE, x, self.depth) for x in range(co.TILES_Y)]

    def _get_base_terrain(self, height: int = co.TILES_Y) -> list[list[Tile]]:
        terrain: list[list[Tile]] = []
        for y in range(height):
            terrain.append([Tile(TileType.BASE, x, y) for x in range(co.TILES_Y)])
        self.depth = height
        return terrain

    def get_level_1_terrain(self):
        terrain = self._get_base_terrain()

        terrain[8][10] = Tile(TileType.NITROGEN, 10, 8)
        terrain[8][10].set_starting_resource(100, 5)

        terrain[8][16] = Tile(TileType.WATER, 16, 8)
        terrain[8][16].set_starting_resource(100, 5)

        terrain[8][22] = Tile(TileType.PHOSPHORUS, 22, 8)
        terrain[8][22].set_starting_resource(100, 5)

        terrain[17][10] = Tile(TileType.ROCK, 17, 10)
        terrain[17][9] = Tile(TileType.ROCK, 17, 9)

        terrain[18][10] = Tile(TileType.WATER, 10, 18)
        terrain[18][10].set_starting_resource(120, 7)

        terrain[18][16] = Tile(TileType.PHOSPHORUS, 16, 18)
        terrain[18][16].set_starting_resource(120, 7)

        terrain[18][22] = Tile(TileType.NITROGEN, 22, 18)
        terrain[18][22].set_starting_resource(120, 7)

        return terrain


    def get_level_2_terrain(self):
        terrain = self._get_base_terrain(co.TILES_Y + 10)

        terrain[34][16] = Tile(TileType.WATER, 16, 34)
        terrain[34][16].set_starting_resource(150, 8)

        return terrain

    def get_level_3_terrain(self):
        terrain = self._get_base_terrain(co.TILES_Y + 10)

        terrain[20][12] = Tile(TileType.PRODUCTION, 12, 20)
        terrain[20][20] = Tile(TileType.CONSUMPTION, 20, 20)

        terrain[25][16] = Tile(TileType.WATER, 16, 25)
        terrain[25][16].set_starting_resource(300, 12)

        return terrain


    def starting_terrain(self) -> list[list[Tile]]:
        return self.get_level_1_terrain()

    def next_level(self):
        self.level += 1

    def show_bonuses(self):
        return True

    def get_level(self, *args):
        return f'{self.level} / {co.TUTORIAL_MAX_LEVEL}'
