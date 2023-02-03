import pygame as pyg
from pygame import Surface
import pyghelper

import constants as co
from generator import TerrainGenerator
from root import RootGhost, Root
from tile import Tile, TileType
import textures as tx


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
        self.is_clicking: bool = False
        self.is_dragging: bool = False
        self.drag_start_y: int = 0
        self.max_height: int = 0

        # Roots
        self.root_ghost: RootGhost = RootGhost()

        self.has_ended = False

    def start(self) -> None:
        self.terrain = self.terrain_generator.starting_terrain()
        self.max_visible_tiles = co.TILES_Y + 500


    def mousedown_game(self, data: dict[str, int]):
        pyg.time.set_timer(pyg.event.Event(pyg.USEREVENT, {'name': 'drag_timer'}), 55, loops=0)
        self.is_clicking = True
        self.drag_start_y = data['pos'][1]

    def mouseup_game(self, data: dict[str, int]):
        self.is_clicking = False
        self.is_dragging = False

        if not self.root_ghost.enabled:
            x = (0.5 + data['pos'][0] // co.TILE) * co.TILE
            y = (0.5 + data['pos'][1] // co.TILE) * co.TILE
            self.root_ghost.enable(x, y)
        else:
            pass

    def mousemove_game(self, data: dict[str, int]):
        if self.is_dragging:
            self.current_height -= data['rel'][1]
            if self.current_height < 0:
                self.current_height = 0
            elif self.current_height + co.HEIGHT > self.max_visible_tiles * co.TILE:
                self.current_height = self.max_visible_tiles * co.TILE - co.HEIGHT
        else:
            self.root_ghost.update_texture(*data['pos'])

    def mousewheel_game(self, data: dict[str, int]):
        self.current_height -= data['y'] * co.TILE
        if self.current_height < 0:
            self.current_height = 0
        elif self.current_height + co.HEIGHT > self.max_visible_tiles * co.TILE:
            self.current_height = self.max_visible_tiles * co.TILE - co.HEIGHT

    def generate_missing(self):
        max_y = self.current_height // co.TILE + co.TILES_Y
        for _ in range(len(self.terrain), max_y):
            self.terrain.append(next(self.terrain_generator))


    def draw_terrain(self):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        game_surface.blit(tx.BACKGROUND, (0, 0))

        # Terrain
        start_y = self.current_height // co.TILE
        for y in range(co.TILES_Y):
            row = self.terrain[y + start_y]
            for x, tile in enumerate(row):
                game_surface.blit(tile.get_texture(), (x * co.TILE, y * co.TILE))


        # RootGhost
        if self.root_ghost.texture_ready:
            game_surface.blit(self.root_ghost.texture, (self.root_ghost.x, self.root_ghost.y))

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
