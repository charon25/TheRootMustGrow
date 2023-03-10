from math import atan2, ceil, cos, dist, sin
from os import getpid
from tkinter import E
from psutil import Process
import random


import pygame as pyg
from pygame import Surface
import pyghelper

import constants as co
from generator import TerrainGenerator
from particle import Particle
from root import compute_crossing_tiles, exact_crossing_tiles, RootGhost, Root
from tile import Tile, TileType
import textures as tx
from tutorial import Tutorial
import utils


process = Process(getpid())


class Game:
    def __init__(self, screen: Surface) -> None:
        # Screen
        self.screen = screen
        def repeat_00():
            while True:
                yield (0, 0)
        self.offset = repeat_00()

        self.setup_sounds()

        self.clock = pyg.time.Clock()

        self.state: co.GameState = co.GameState.MENU

        # Events
        self.events = pyghelper.EventManager(True)
        self.events.set_quit_callback(self.stop)
        self.set_callbacks()

        self.tutorial_done: bool = False
        try:
            with open('tuto.txt', 'r') as fi:
                pass
            self.tutorial_done = True
        except Exception:
            pass

        def does_drag(data):self.is_dragging = self.is_clicking
        self.events.add_custom_event('drag_timer', does_drag)

        self.has_ended = False


    def setup_sounds(self):
        self.sounds: pyghelper.SoundManager = pyghelper.SoundManager()
        self.sounds.add_sound(co.SOUND_CLICK_PATH, co.SOUND_CLICK, volume=0.4)
        utils.add_multiple_sounds(self.sounds, co.SOUND_ROOT_GROW_PATHS, co.SOUND_ROOT_GROW, volume=0.6)
        utils.add_multiple_sounds(self.sounds, co.SOUND_ROOT_CUT_PATHS, co.SOUND_ROOT_CUT, volume=0.6)
        utils.add_multiple_sounds(self.sounds, co.SOUND_ROOT_DIE_PATHS, co.SOUND_ROOT_DIE, volume=0.6)
        self.sounds.add_sound(co.SOUND_BONUS_PATH, co.SOUND_BONUS, volume=0.5)
        utils.add_multiple_sounds(self.sounds, co.SOUND_WATER_PATHS, co.SOUND_WATER, volume=0.45)
        utils.add_multiple_sounds(self.sounds, co.SOUND_RESOURCE_PATHS, co.SOUND_RESOURCE, volume=0.45)
        self.sounds.add_sound(co.SOUND_TUTO_PAGE_PATH, co.SOUND_TUTO_PAGE, volume=0.5)
        self.sounds.add_sound(co.SOUND_TUTO_END_PATH, co.SOUND_TUTO_END, volume=0.5)
        self.sounds.add_sound(co.SOUND_LOSE_PATH, co.SOUND_LOSE, volume=0.75)
        self.sounds.add_sound(co.SOUND_WARNING_PATH, co.SOUND_WARNING, volume=0.3)

        self.sounds.add_music(co.MUSIC_PATH, co.MUSIC)
        self.sounds.play_music(co.MUSIC, loop=True, volume=0.05)

    def start_game(self, tutorial: bool) -> None:
        # Terrain
        if not tutorial:
            self.state = co.GameState.GAME
            self.terrain_generator = TerrainGenerator()
            self.max_visible_tiles = co.TILES_Y + co.STARTING_SCROLL_OFFSET
            self.resources: dict[co.ResourceType, int] = {resource: co.RESOURCES_START[resource] for resource in list(co.ResourceType)}

        else:
            self.state = co.GameState.TUTORIAL
            self.terrain_generator = Tutorial()
            self.max_visible_tiles = co.TILES_Y
            self.resources: dict[co.ResourceType, int] = {resource: 100 for resource in list(co.ResourceType)}

        self.terrain: list[list[Tile]] = self.terrain_generator.starting_terrain()

        self.selected_tile: tuple[int, int] = (-1, -1)
        ## Drag
        self.current_height: int = 0
        self.current_height_floored: int = 0
        self.is_clicking: bool = False
        self.is_dragging: bool = False
        self.drag_start_y: int = 0
        self.max_height: int = 0

        # Ressources
        self.resources_tiles: list[Tile] = list()
        self.absorption_rate: dict[co.ResourceType, float] = co.STARTING_ABSORPTION_RATE.copy()
        self.consumption_rate: dict[co.ResourceType, float] = co.STARTING_CONSUMPTION_RATE.copy()
        self.total_gained: dict[co.ResourceType, float] = {resource: 0 for resource in co.ResourceType}
        self.total_consummed: dict[co.ResourceType, float] = {resource: 0 for resource in co.ResourceType}
        # Bonus
        self.production_bonus: float = 0
        self.consumption_bonus: float = 1

        # Roots
        self.root_ghost: RootGhost = RootGhost()
        self.roots: list[Root] = list()
        self.decay_cooldown = -1
        self.root_id = 0
        self.total_roots: float = 0

        # Particules
        self.particles: list[Particle] = list()

        self.ticks = 0
        self.memory_usage = process.memory_info().rss

        self.set_callbacks()
        self.create_initial_roots()

    def set_callbacks(self):
        if self.state == co.GameState.MENU:
            self.events.set_mousebuttondown_callback(utils.void)
            self.events.set_mousebuttonup_callback(self.mouseup_menu)
            self.events.set_mousemotion_callback(utils.void)
            self.events.set_mousewheel_callback(utils.void)
        elif self.state in (co.GameState.GAME, co.GameState.TUTORIAL):
            self.events.set_mousebuttondown_callback(self.mousedown_game)
            self.events.set_mousebuttonup_callback(self.mouseup_game)
            self.events.set_mousemotion_callback(self.mousemove_game)
            self.events.set_mousewheel_callback(self.mousewheel_game)


    def mouseup_menu(self, data: dict[str, int]):
        if not data['button'] in (co.LEFT_CLICK, co.RIGHT_CLICK):
            return

        if utils.point_in_rectangle(*data['pos'], co.QUIT_BTN_X, co.QUIT_BTN_Y, co.BTN_WIDTH, co.BTN_HEIGHT):
            self.stop()
        elif utils.point_in_rectangle(*data['pos'], co.TUTO_BTN_X, co.TUTO_BTN_Y, co.BTN_WIDTH, co.BTN_HEIGHT):
            self.sounds.play_sound(co.SOUND_CLICK)
            self.tutorial_done = False
            self.start_game(tutorial=True)
        elif self.tutorial_done and utils.point_in_rectangle(*data['pos'], co.PLAY_BTN_X, co.PLAY_BTN_Y, co.BTN_WIDTH, co.BTN_HEIGHT):
            self.sounds.play_sound(co.SOUND_CLICK)
            self.start_game(tutorial=False)


    def create_initial_roots(self):
        root_ghost = RootGhost()
        root_ghost.enable(co.WIDTH // 2 + co.TILE // 2, co.TILE // 2, None)
        root_ghost.set_endpoint(co.WIDTH // 2 + co.TILE // 2, 100 + co.TILE // 2)
        self.create_root_from_ghost(root_ghost, root_ghost.end_x, root_ghost.end_y, auto=True)


    def mousedown_game(self, data: dict[str, int]):
        if data['button'] == co.LEFT_CLICK:
            pyg.time.set_timer(pyg.event.Event(pyg.USEREVENT, {'name': 'drag_timer'}), 100, loops=1)
            self.is_clicking = True
            self.drag_start_y = data['pos'][1]
        elif data['button'] == co.RIGHT_CLICK:
            self.root_ghost.disable()

    def get_crossing_tile_root_ghost(self, root_ghost: RootGhost, mouse_x: int, mouse_y: int) -> list[tuple[int, int]]:
        return exact_crossing_tiles(
            root_ghost.start_x,
            root_ghost.start_y,
            mouse_x,
            mouse_y
        )

    def get_exact_crossing_tile_root_ghost(self, root_ghost: RootGhost, mouse_x: int, mouse_y: int) -> list[tuple[int, int]]:
        return exact_crossing_tiles(
            root_ghost.start_x,
            root_ghost.start_y,
            mouse_x,
            mouse_y
        )

    def apply_bonus(self, tile: Tile):
        bonus_type = co.BonusType(tile.type.value)
        if bonus_type == co.BonusType.PRODUCTION:
            self.production_bonus += tile.bonus_value

        if bonus_type == co.BonusType.CONSUMPTION:
            self.consumption_bonus *= (1 + tile.bonus_value)

    def create_root_from_ghost(self, root_ghost: RootGhost, mouse_x: int, mouse_y: int, auto: bool = False) -> bool:
        crossing_tiles = self.get_crossing_tile_root_ghost(root_ghost, mouse_x, mouse_y)
        new_root = Root(self.root_id, root_ghost, crossing_tiles, not_cuttable=auto)
        self.root_id += 1

        for x_cross, y_cross in crossing_tiles:
            self.terrain[y_cross][x_cross].has_root = True
            self.terrain[y_cross][x_cross].root = new_root

        if not auto:
            self.sounds.play_sound(co.SOUND_ROOT_GROW)

            self.offset = self.screen_shake(utils.clamped_lerp(new_root.length, 0, co.SCREENSHAKE_LENGTH_MAX, 0, co.SCREENSHAKE_AMOUNT_MAX))

            mouse_tile_x, mouse_tile_y = mouse_x // co.TILE, mouse_y // co.TILE
            tile = self.terrain[mouse_tile_y][mouse_tile_x]
            if tile.is_resource_tile():
                self.sounds.play_sound(co.SOUND_WATER if tile.type == TileType.WATER else co.SOUND_RESOURCE)
                self.resources_tiles.append(tile)
                new_root.resource_tile = tile
            elif tile.is_bonus_tile():
                self.sounds.play_sound(co.SOUND_BONUS)
                self.apply_bonus(tile)
                self.particles.extend(Particle.generate_bonus_particles(tile.x * co.TILE + co.TILE / 2, tile.y * co.TILE + co.TILE / 2, tile.type))
                tile.type = TileType.BASE
                self.offset = self.screen_shake(co.BONUS_SCREENSHAKE)

            if self.state == co.GameState.GAME and  mouse_tile_y + co.MAX_VISIBLE_TILES_OFFSET > self.max_visible_tiles:
                self.max_visible_tiles = mouse_tile_y + co.MAX_VISIBLE_TILES_OFFSET

            new_root.parent.increase_width()


        self.roots.append(new_root)
        return True

    def create_root_ghost(self, mouse_x: int, mouse_y: int):
        tile_x, tile_y = mouse_x // co.TILE, (mouse_y + self.current_height_floored) // co.TILE

        tile = self.terrain[tile_y][tile_x]

        if not tile.has_root:
            return

        if not tile.root.contains_point(mouse_x, mouse_y + self.current_height_floored):
            return

        x = co.TILE / 2 + utils.floor_n(mouse_x, co.TILE)
        y = co.TILE / 2 + utils.floor_n(mouse_y, co.TILE)

        if tile.root.parent is not None and tile.root.parent.contains_point(mouse_x, mouse_y + self.current_height_floored):
            self.root_ghost.enable(x, y + self.current_height_floored, tile.root.parent)
        else:
            self.root_ghost.enable(x, y + self.current_height_floored, tile.root)

    def delete_root(self, deleted_root: Root, is_dead: bool):
            if deleted_root.not_cuttable or deleted_root.parent is None:
                return

            if any(root.is_child(deleted_root) for root in self.roots if root is not deleted_root):
                return

            for x_cross, y_cross in deleted_root.crossing_tiles:
                if not (x_cross, y_cross) in deleted_root.parent.crossing_tiles:
                    self.terrain[y_cross][x_cross].has_root = False
                    self.terrain[y_cross][x_cross].root = None
                else:
                    self.terrain[y_cross][x_cross].root = deleted_root.parent

            if deleted_root.resource_tile is not None:
                try:
                    self.resources_tiles.remove(deleted_root.resource_tile)
                except ValueError:
                    pass

            if self.root_ghost.enabled and self.root_ghost.starting_root is deleted_root:
                self.root_ghost.disable()

            try:
                self.roots.remove(deleted_root)
            except ValueError:
                pass
            else:
                if not is_dead:
                    self.sounds.play_sound(co.SOUND_ROOT_CUT)
                else:
                    self.sounds.play_sound(co.SOUND_ROOT_DIE)
                self.offset = self.screen_shake(co.SCREENSHAKE_AMOUNT_MAX)

    def mouseup_game(self, data: dict[str, int]):
        if data['button'] == co.LEFT_CLICK:
            self.is_clicking = False

            if not self.root_ghost.enabled:
                self.create_root_ghost(*data['pos'])
            else:
                if not self.is_dragging and self.root_ghost.correct:
                    x = co.TILE / 2 + utils.floor_n(data['pos'][0], co.TILE)
                    y = co.TILE / 2 + utils.floor_n(data['pos'][1], co.TILE)
                    self.root_ghost.set_endpoint(x, y + self.current_height_floored)
                    self.create_root_from_ghost(self.root_ghost, data['pos'][0], data['pos'][1] + self.current_height_floored)
                    self.root_ghost.disable()

            self.is_dragging = False
        elif data['button'] == co.RIGHT_CLICK and not self.root_ghost.enabled:
            mouse_x, mouse_y = data['pos']
            tile_x, tile_y = mouse_x // co.TILE, (mouse_y + self.current_height_floored) // co.TILE

            if not self.terrain[tile_y][tile_x].has_root:
                return

            if not self.terrain[tile_y][tile_x].root.contains_point(mouse_x, mouse_y + self.current_height):
                return

            cut_root = self.terrain[tile_y][tile_x].root
            self.delete_root(cut_root, False)


    def scroll_screen(self, quantity: int):
        self.current_height -= quantity
        if self.current_height < 0:
            self.current_height = 0
        elif self.current_height + co.HEIGHT > self.max_visible_tiles * co.TILE:
            self.current_height = self.max_visible_tiles * co.TILE - co.HEIGHT

        self.current_height_floored = utils.floor_n(self.current_height, co.TILE)

        x, y = pyg.mouse.get_pos()
        self.root_ghost.set_endpoint(x, y + self.current_height)

    def is_root_ghost_correct(self, mouse_x: int, mouse_y: int):
        if mouse_y - self.current_height >= co.HEIGHT - co.UI_HEIGHT * co.TILE:
            return False

        if mouse_y // co.TILE <= self.root_ghost.start_y // co.TILE:
            return False

        tile_x, tile_y = mouse_x // co.TILE, mouse_y // co.TILE
        tile = self.terrain[tile_y][tile_x]

        if tile.has_root and tile.root.contains_point(mouse_x, mouse_y):
            return False

        for cross_x, cross_y in self.get_crossing_tile_root_ghost(self.root_ghost, mouse_x, mouse_y):
            if (cross_x, cross_y) == (self.root_ghost.start_x // co.TILE, self.root_ghost.start_y // co.TILE):
                continue
            tile = self.terrain[cross_y][cross_x]
            if tile.has_root and not self.root_ghost.starting_root.is_child(tile.root):
                return False

        for tile_x, tile_y in self.get_exact_crossing_tile_root_ghost(self.root_ghost, mouse_x, mouse_y):
            tile = self.terrain[tile_y][tile_x]
            if tile.type == TileType.ROCK:
                return False

        return True

    def mousemove_game(self, data: dict[str, int]):
        if self.is_dragging:
            self.scroll_screen(data['rel'][1])
        elif self.root_ghost.enabled:
            mouse_x, mouse_y = data['pos'][0], data['pos'][1] + self.current_height
            length = self.root_ghost.get_length(mouse_x, mouse_y)
            if length < co.MAX_ROOT_LENGTH:
                self.root_ghost.set_endpoint(mouse_x, mouse_y)
                self.root_ghost.correct = self.is_root_ghost_correct(mouse_x, mouse_y)

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


    def screen_shake(self, amount):
        for _ in range(co.SCREENSHAKE_COUNT):
            x, y = utils.random_sym_float(amount), utils.random_sym_float(amount)
            yield (x, y)
        while True:
            yield (0, 0)


    def blit_overlined_text(self, game_surface: Surface, text: str, font: pyg.font.Font, x: float, y: float, center_x: bool = False):
        black_text_surface = font.render(text, False, (0, 0, 0))
        white_text_surface = font.render(text, False, (255, 255, 255))

        if center_x:
            x -= white_text_surface.get_width() / 2

        game_surface.blit(white_text_surface, (x + 1, y + 1))
        game_surface.blit(white_text_surface, (x + 1, y - 1))
        game_surface.blit(white_text_surface, (x - 1, y + 1))
        game_surface.blit(white_text_surface, (x - 1, y - 1))

        game_surface.blit(black_text_surface, (x, y))


    def draw_terrain(self):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        pyg.draw.rect(game_surface, (0, 0, 0), pyg.Rect(0, 0, co.WIDTH, co.HEIGHT))

        # Terrain
        start_y = self.current_height // co.TILE

        resource_tiles: list[Tile] = []
        bonus_tiles: list[Tile] = []

        for y in range(co.TILES_Y - co.UI_HEIGHT):
            row = self.terrain[y + start_y]
            for x, tile in enumerate(row):
                game_surface.blit(tile.texture, (x * co.TILE, y * co.TILE))
                if tile.type != TileType.BASE:
                    has_resources = tile.is_resource_tile() and tile.resource > 0
                    is_bonus = tile.is_bonus_tile() and tile.bonus_value is not None
                    if has_resources:
                        resource_tiles.append(tile)
                    elif is_bonus:
                        bonus_tiles.append(tile)

                    if has_resources or tile.type == TileType.ROCK or tile.is_bonus_tile():
                        game_surface.blit(tile.resource_textures, (x * co.TILE, y * co.TILE))
                if (x, y + start_y) == self.selected_tile:
                    game_surface.blit(tx.TILE_SELECTOR, (x * co.TILE, y * co.TILE))# - self.current_height_floored))

        if self.state == co.GameState.TUTORIAL:
            resource_tiles: list[Tile] = []
            for row in self.terrain:
                for tile in row:
                    if tile.is_resource_tile() and tile.resource > 0:
                        resource_tiles.append(tile)

        # Roots
        for root in self.roots:
            if root.is_visible(self.current_height_floored):
                root._update_texture()
                game_surface.blit(root.texture, (root.x, root.y - self.current_height_floored))
            root.overlined = False

        # Tuto
        font = utils.get_font(30)
        if self.state == co.GameState.TUTORIAL:
            level = self.terrain_generator.level
            lines = co.TUTORIAL_TEXTS[level]
            y = co.TUTORIAL_TEXT_Y_START
            for line in lines:
                self.blit_overlined_text(game_surface, line, font, co.TUTORIAL_TEXT_X, y, False)
                y += 20

        # Particules

        game_surface.blits([(particle.texture, (particle.x, particle.y - self.current_height_floored)) for particle in self.particles if particle.is_visible(self.current_height_floored) and not particle.is_fixed])

        # Resources
        font = utils.get_font(15)
        for tile in resource_tiles:
            x = tile.x * co.TILE + co.TILE / 2 + 1
            y = tile.y * co.TILE - 2 - self.current_height_floored
            if 1_000 > tile.resource >= 0:
                resource_str = str(ceil(tile.resource))
            elif 1_000_000 > tile.resource >= 1_000:
                resource_str = utils.get_resource_string(tile.resource, 1_000, 'K')
            elif 1_000_000_000 > tile.resource >= 1_000_000:
                resource_str = utils.get_resource_string(tile.resource, 1_000_000, 'M')
            elif tile.resource >= 1_000_000_000:
                resource_str = utils.get_resource_string(tile.resource, 1_000_000_000, 'B')

            self.blit_overlined_text(game_surface, resource_str, font, x, y, center_x = True)

        if self.state == co.GameState.TUTORIAL and len(resource_tiles) == 0:
            if self.terrain_generator.level == 1:
                self.current_height = 0
                self.current_height_floored = 0
                self.terrain = self.terrain_generator.get_level_2_terrain()
                self.max_visible_tiles = co.TILES_Y + 10
            elif self.terrain_generator.level == 2:
                self.current_height = 0
                self.current_height_floored = 0
                self.terrain = self.terrain_generator.get_level_3_terrain()
                self.max_visible_tiles = co.TILES_Y
            elif self.terrain_generator.level == 3:
                self.sounds.play_sound(co.SOUND_TUTO_END)
                self.current_height = 0
                self.current_height_floored = 0
                self.tutorial_done = True
                try:
                    with open('tuto.txt', 'w') as fo:
                        fo.write('done')
                    self.tutorial_done = True
                except Exception:
                    pass
                self.state = co.GameState.MENU
                self.set_callbacks()
                return

            self.sounds.play_sound(co.SOUND_TUTO_PAGE)
            self.terrain_generator.level += 1
            self.roots = []
            self.create_initial_roots()

        # Bonus
        font = utils.get_font(15)
        for tile in bonus_tiles:
            x = tile.x * co.TILE + co.TILE / 2 + 1
            y = tile.y * co.TILE - 2 - self.current_height_floored

            self.blit_overlined_text(game_surface, f'{abs(100 * tile.bonus_value):.0f} %', font, x, y, center_x = True)


        # RootGhost
        if self.root_ghost.texture_ready:
            game_surface.blit(self.root_ghost.texture, (self.root_ghost.x, self.root_ghost.y - self.current_height_floored))

        # UI
        game_surface.blit(tx.UI_BACKGROUND, (0, co.UI_TOP))

        font = utils.get_font(25)
        for resource in co.ResourceType:
            resource_text_surface = font.render(f'{co.RESOURCE_TEXT_NAME[resource]}{co.RESOURCE_SPACES[resource]}  {utils.int_to_small_string(self.resources[resource], 1, True)} (- {utils.int_to_small_string(self.total_consummed[resource] * 60, 2)}/s) (+ {utils.int_to_small_string(self.total_gained[resource] * 60, 2)}/s)', False, (0, 0, 0))
            x, y = co.RESOURCE_TEXT_COORDS[resource]
            game_surface.blit(resource_text_surface, (x, y + co.UI_TOP + co.TILE / 2 - resource_text_surface.get_height() / 2))



        total_resources_text_surface = font.render(f'Total roots : {self.total_roots / co.TILE:.0f}', False, (0, 0, 0))
        game_surface.blit(total_resources_text_surface, (co.TOTAL_ROOTS_TEXT_COORD[0], co.TOTAL_ROOTS_TEXT_COORD[1] + co.UI_TOP))

        self.blit_overlined_text(game_surface, f'Depth : {self.current_height_floored // co.TILE + co.TILES_Y - co.UI_HEIGHT:.0f} / {self.max_visible_tiles - co.UI_HEIGHT} [{self.terrain_generator.get_level(self.current_height_floored // co.TILE + co.TILES_Y - co.UI_HEIGHT)}]', utils.get_font(30), *co.DEPTH_COORDS)

        game_surface.blits([(particle.texture, (particle.x, particle.y)) for particle in self.particles if particle.is_fixed])

        if self.state == co.GameState.GAME or (self.state == co.GameState.TUTORIAL and self.terrain_generator.show_bonuses()):
            font = utils.get_font(30)
            bonus_text_surface = font.render(f'Bonuses :', False, (0, 0, 0))
            game_surface.blit(bonus_text_surface, (co.BONUS_TEXT_COORD[0], co.BONUS_TEXT_COORD[1] + co.UI_TOP))

            font = utils.get_font(25)
            if self.production_bonus < 1:
                production_bonus_text_surface = font.render(f'Production    +{self.production_bonus * 100:.1f} %', False, (0, 0, 0))
            else:
                production_bonus_text_surface = font.render(f'Production    x{(1 + self.production_bonus):.2f}', False, (0, 0, 0))
            game_surface.blit(production_bonus_text_surface, (co.PRODUCTION_BONUS_TEXT_COORD[0], co.PRODUCTION_BONUS_TEXT_COORD[1] + co.UI_TOP))
            consumption_bonus_text_surface = font.render(f'Consumption   {"-" if self.consumption_bonus == 0 else ""}{(self.consumption_bonus - 1) * 100:.1f} %', False, (0, 0, 0))
            game_surface.blit(consumption_bonus_text_surface, (co.CONSUMPTION_BONUS_TEXT_COORD[0], co.CONSUMPTION_BONUS_TEXT_COORD[1] + co.UI_TOP))

        font = utils.get_font(16)
        fps_text_surface = font.render(f'{self.fps:.0f} FPS', False, (0, 0, 0))
        game_surface.blit(fps_text_surface, (co.FPS_COORDS[0], co.FPS_COORDS[1] + co.UI_TOP))

        memory_text_surface = font.render(f'{self.memory_usage / (1024 * 1024):.1f} Mio', False, (0, 0, 0))
        game_surface.blit(memory_text_surface, (co.MEMORY_COORDS[0], co.MEMORY_COORDS[1] + co.UI_TOP))


        # Fin
        self.screen.blit(game_surface, next(self.offset))


    def update_resources(self):
        self.total_gained = {resource: 0 for resource in co.ResourceType}
        for tile in self.resources_tiles:
            if tile.resource >= 0:
                resource = co.ResourceType(tile.type.value)
                self.particles.extend(Particle.generate_extract_particle(tile.x * co.TILE + co.TILE / 2, tile.y * co.TILE + co.TILE / 2, tile.type))
                consumed = tile.consume(self.absorption_rate[resource] * (1 + self.production_bonus))
                self.resources[resource] += consumed
                self.total_gained[resource] += consumed

                if tile.resource == 0:
                    tile.root.resource_tile = None

        self.total_roots = sum(root.length for root in self.roots)
        for resource in co.ResourceType:
            consumed = self.total_roots * self.consumption_rate[resource] * self.consumption_bonus
            self.resources[resource] -= consumed
            self.total_consummed[resource] = consumed

            show_particle = random.random() < utils.clamped_lerp(self.total_gained[resource], 0, co.GAINED_RESOURCE_PARTICLE_MAX_PROBABILITY_AMOUNT, co.GAINED_RESOURCE_PARTICLE_MIN_PROBABILITY, co.GAINED_RESOURCE_PARTICLE_MAX_PROBABILITY)
            if self.total_gained[resource] > 0 and show_particle:
                self.particles.extend(Particle.generate_extract_particle(*co.UI_RESOURCE_TEXTURE_COORDS[resource], TileType(resource.value), fixed=True))

        if any(quantity <= 0 and self.total_gained[resource] < self.total_consummed[resource] for resource, quantity in self.resources.items()):
            if self.decay_cooldown < 0:
                smallest_resource = min(quantity for _, quantity in self.resources.items())
                self.decay_cooldown = utils.clamped_lerp(smallest_resource, co.MIN_DECAY_COOLDOWN_RESOURCE, 0, co.MIN_DECAY_COOLDOWN, co.STARTING_DECAY_COOLDOWN)
        else:
            self.decay_cooldown = -1

        self.resources_tiles = [tile for tile in self.resources_tiles if tile.resource > 0]


    def update_roots(self):
        if self.state != co.GameState.GAME:
            return

        if int(self.decay_cooldown) % 100 == 45:
            self.sounds.play_sound(co.SOUND_WARNING)

        if self.decay_cooldown > 0:
            self.decay_cooldown -= 1

        if -1 < self.decay_cooldown < 0:
            if len(self.roots) <= 1:
                self.game_over()
            self.delete_root(self.roots[-1], True)
            self.decay_cooldown = -1

    def check_mouse_over_root(self):
        mouse_x, mouse_y = pyg.mouse.get_pos()

        if mouse_y > co.UI_TOP:
            self.selected_tile = (-1, -1)
            return

        mouse_tile_x, mouse_tile_y = mouse_x // co.TILE, (mouse_y + self.current_height) // co.TILE
        self.selected_tile = (mouse_tile_x, mouse_tile_y)
        tile = self.terrain[mouse_tile_y][mouse_tile_x]

        if not tile.has_root:
            return

        if tile.root.contains_point(mouse_x, mouse_y + self.current_height):
            tile.root.overlined = True

    def game_over(self):
        self.sounds.play_sound(co.SOUND_LOSE)
        self.state = co.GameState.MENU
        self.set_callbacks()

    def loop_game(self):
        self.generate_missing()

        self.check_mouse_over_root()

        self.update_resources()
        self.update_roots()

        for particle in self.particles:
            particle.age()
            if particle.done:
                self.particles.remove(particle)

        if self.ticks == 60:
            self.ticks = 0
            self.memory_usage = process.memory_info().rss

        self.draw_terrain()

        self.ticks += 1


    def loop_tutorial(self):
        pass


    def loop(self) -> None:
        dt = self.clock.tick(60)
        self.fps = 1000 / dt
        self.events.listen()

        if self.state == co.GameState.MENU:
            self.screen.blit(tx.MENU_TUTO if not self.tutorial_done else tx.MENU, (0, 0))
        elif self.state in (co.GameState.TUTORIAL, co.GameState.GAME):
            self.loop_game()

        pyg.display.update()

    def stop(self) -> None:
        self.has_ended = True
        pass
