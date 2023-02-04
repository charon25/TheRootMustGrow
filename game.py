from math import atan2, cos, dist, sin
import pygame as pyg
from pygame import Surface
import pyghelper

import constants as co
from generator import TerrainGenerator
from root import compute_crossing_tiles, RootGhost, Root
from tile import Tile, TileType
import textures as tx
from utils import floor_n




class Game:
    def __init__(self, screen: Surface) -> None:
        # Screen
        self.screen = screen
        def repeat_00():
            while True:
                yield (0, 0)
        self.offset = repeat_00()

        self.clock = pyg.time.Clock()
        # Events
        self.events = pyghelper.EventManager(True)
        self.events.set_quit_callback(self.stop)
        self.events.set_mousebuttondown_callback(self.mousedown_game)
        self.events.set_mousebuttonup_callback(self.mouseup_game)
        self.events.set_mousemotion_callback(self.mousemove_game)
        self.events.set_mousewheel_callback(self.mousewheel_game)

        def does_drag(data):self.is_dragging = self.is_clicking
        self.events.add_custom_event('drag_timer', does_drag)

        # Terrain
        self.terrain_generator = TerrainGenerator()
        self.terrain: list[list[Tile]] = list()
        ## Drag
        self.current_height: int = 0
        self.current_height_floored: int = 0
        self.is_clicking: bool = False
        self.is_dragging: bool = False
        self.drag_start_y: int = 0
        self.max_height: int = 0

        # Roots
        self.root_ghost: RootGhost = RootGhost()
        self.roots: list[Root] = list()

        self.has_ended = False

    def start(self) -> None:
        self.terrain = self.terrain_generator.starting_terrain()
        self.max_visible_tiles = co.TILES_Y + 500
        self.create_initial_roots()

    def create_initial_roots(self):
        root_ghost = RootGhost()
        root_ghost.enable(co.WIDTH // 2 + co.TILE // 2, co.TILE // 2, None)
        root_ghost.set_endpoint(co.WIDTH // 2 + co.TILE // 2, 100 + co.TILE // 2)
        self.create_root_from_ghost(root_ghost, root_ghost.end_x, root_ghost.end_y)


    def mousedown_game(self, data: dict[str, int]):
        if data['button'] == co.LEFT_CLICK:
            pyg.time.set_timer(pyg.event.Event(pyg.USEREVENT, {'name': 'drag_timer'}), 100, loops=1)
            self.is_clicking = True
            self.drag_start_y = data['pos'][1]
        elif data['button'] == co.RIGHT_CLICK:
            self.root_ghost.disable()

    def get_crossing_tile_root_ghost(self, root_ghost: RootGhost, mouse_x: int, mouse_y: int) -> list[tuple[int, int]]:
        return compute_crossing_tiles(
            int(root_ghost.start_x // co.TILE),
            int(root_ghost.start_y // co.TILE),
            mouse_x // co.TILE,
            mouse_y // co.TILE
        )

    def create_root_from_ghost(self, root_ghost: RootGhost, mouse_x: int, mouse_y: int) -> bool:
        crossing_tiles = self.get_crossing_tile_root_ghost(root_ghost, mouse_x, mouse_y)
        new_root = Root(root_ghost, crossing_tiles)

        for x_cross, y_cross in crossing_tiles:
            if not self.terrain[y_cross][x_cross].has_root:
                self.terrain[y_cross][x_cross].type = TileType.ROOT # TODO temporary line
                self.terrain[y_cross][x_cross].has_root = True
                self.terrain[y_cross][x_cross].root = new_root

        self.roots.append(new_root)
        return True

    def create_root_ghost(self, mouse_x: int, mouse_y: int):
        tile_x, tile_y = mouse_x // co.TILE, (mouse_y + self.current_height_floored) // co.TILE
        print(mouse_x, mouse_y, mouse_x // co.TILE, mouse_y // co.TILE)
        if not self.terrain[tile_y][tile_x].has_root:
            print('no root')
            return
        if not self.terrain[tile_y][tile_x].root.contains_point(mouse_x, mouse_y + self.current_height):
            print('no contains')
            return

        x = co.TILE / 2 + floor_n(mouse_x, co.TILE)
        y = co.TILE / 2 + floor_n(mouse_y, co.TILE)
        self.root_ghost.enable(x, y + self.current_height_floored, self.terrain[tile_y][tile_x].root)

    def mouseup_game(self, data: dict[str, int]):
        if data['button'] != co.LEFT_CLICK:
            return

        self.is_clicking = False

        if not self.root_ghost.enabled:
            self.create_root_ghost(*data['pos'])
        else:
            if not self.is_dragging and self.root_ghost.correct:
                x = co.TILE / 2 + floor_n(data['pos'][0], co.TILE)
                y = co.TILE / 2 + floor_n(data['pos'][1], co.TILE)
                self.root_ghost.set_endpoint(x, y + self.current_height_floored)
                self.create_root_from_ghost(self.root_ghost, data['pos'][0], data['pos'][1] + self.current_height_floored)
                self.root_ghost.disable()

        self.is_dragging = False

    def scroll_screen(self, quantity: int):
        self.current_height -= quantity
        if self.current_height < 0:
            self.current_height = 0
        elif self.current_height + co.HEIGHT > self.max_visible_tiles * co.TILE:
            self.current_height = self.max_visible_tiles * co.TILE - co.HEIGHT

        self.current_height_floored = floor_n(self.current_height, co.TILE)

        x, y = pyg.mouse.get_pos()
        self.root_ghost.set_endpoint(x, y + self.current_height)

    def mousemove_game(self, data: dict[str, int]):
        if self.is_dragging:
            self.scroll_screen(data['rel'][1])
        elif self.root_ghost.enabled:
            mouse_x, mouse_y = data['pos'][0], data['pos'][1] + self.current_height
            length = self.root_ghost.set_length(mouse_x, mouse_y)
            if length < co.MAX_ROOT_LENGTH:
                self.root_ghost.set_endpoint(mouse_x, mouse_y)
                self.root_ghost.correct = True
                for tile_x, tile_y in self.get_crossing_tile_root_ghost(self.root_ghost, mouse_x, mouse_y):
                    if self.terrain[tile_y][tile_x].has_root and not self.terrain[tile_y][tile_x].root is self.root_ghost.starting_root:
                        self.root_ghost.correct = False
                        break
                if mouse_y // co.TILE <= self.root_ghost.start_y // co.TILE:
                    self.root_ghost.correct = False
            else:
                angle = -atan2(mouse_y - self.root_ghost.start_y, mouse_x - self.root_ghost.start_x)
                end_x = int(self.root_ghost.start_x + cos(angle) * co.MAX_ROOT_LENGTH)
                end_y = int(self.root_ghost.start_y - sin(angle) * co.MAX_ROOT_LENGTH)
                self.root_ghost.set_endpoint(end_x, end_y)
                self.root_ghost.correct = False

    def mousewheel_game(self, data: dict[str, int]):
        self.scroll_screen(data['y'] * co.TILE)

    def generate_missing(self):
        max_y = self.current_height // co.TILE + co.TILES_Y
        for _ in range(len(self.terrain), max_y + 1):
            self.terrain.append(next(self.terrain_generator))


    def draw_terrain(self):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        game_surface.blit(tx.BACKGROUND, (0, 0))

        # Terrain
        start_y = self.current_height // co.TILE
        # range_len = co.TILES_Y + 1
        # if start_y > 0:
        #     start_y -= 1
        #     range_len += 1

        for y in range(co.TILES_Y):
            row = self.terrain[y + start_y]
            for x, tile in enumerate(row):
                game_surface.blit(tile.get_texture(), (x * co.TILE, y * co.TILE))

        # Roots
        for root in self.roots:
            if root.is_visible(self.current_height_floored):
                game_surface.blit(root.texture, (root.x, root.y - self.current_height_floored))

        # RootGhost
        if self.root_ghost.texture_ready:
            game_surface.blit(self.root_ghost.texture, (self.root_ghost.x, self.root_ghost.y - self.current_height_floored))

        # x_offset, y_offset = next(self.offset)
        # y_offset += (self.current_height % co.TILE)
        self.screen.blit(game_surface, next(self.offset))


    def loop(self) -> None:
        self.clock.tick(60)
        self.events.listen()

        self.generate_missing()

        self.draw_terrain()

        pyg.display.update()

    def stop(self) -> None:
        self.has_ended = True
        pass
