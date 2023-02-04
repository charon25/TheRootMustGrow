from math import atan2, cos, dist, pi, sin

from bresenham import bresenham
import pygame as pyg
from pygame import Surface

import constants as co
import textures as tx
from utils import floor_n


# Pas très efficace
def compute_crossing_tiles(start_tile_x: int, start_tile_y: int, end_tile_x: int, end_tile_y: int):
    points = set()
    points.update(bresenham(start_tile_x, start_tile_y, end_tile_x, end_tile_y))
    points.update(bresenham(start_tile_x - 1, start_tile_y, end_tile_x - 1, end_tile_y))
    points.update(bresenham(start_tile_x + 1, start_tile_y, end_tile_x + 1, end_tile_y))
    points.update(bresenham(start_tile_x, start_tile_y - 1, end_tile_x, end_tile_y - 1))
    points.update(bresenham(start_tile_x, start_tile_y + 1, end_tile_x, end_tile_y + 1))
    return list(points)


class Root:
    def __init__(self, root_ghost: 'RootGhost', crossing_tiles: list[tuple[int, int]]) -> None:
        self.x: int = root_ghost.x
        self.y: int = root_ghost.y
        self.start_x: int = root_ghost.start_x
        self.start_y: int = root_ghost.start_y
        self.end_x: int = root_ghost.end_x
        self.end_y: int = root_ghost.end_y
        self.texture: Surface = root_ghost.texture
        self.texture_height = self.texture.get_height()
        self.width: int = 1
        self.crossing_tiles: list[tuple[int, int]] = list()
        self.parent: 'Root' = root_ghost.starting_root
        self.length = root_ghost.get_length(self.end_x, self.end_y)
        self.is_dead = False

    def in_boundary(self, x: int, y:int) -> bool:
        sx, ex = min(self.start_x, self.end_x), max(self.start_x, self.end_x)

        start_x, end_x = floor_n(sx, co.TILE), floor_n(ex, co.TILE) + co.TILE
        start_y, end_y = floor_n(self.start_y, co.TILE), floor_n(self.end_y, co.TILE) + co.TILE

        print(start_x, x, end_x)
        print(start_y, y, end_y)

        if not (start_x <= x <= end_x) or not (start_y <= y <= end_y):
            return False
        return True

    def contains_point(self, x: int, y: int) -> bool:
        if not self.in_boundary(x, y):
            print('no boundary')
            return False

        start_x, start_y = (0.5 + self.start_x // co.TILE) * co.TILE, (0.5 + self.start_y // co.TILE) * co.TILE
        end_x, end_y = (0.5 + self.end_x // co.TILE) * co.TILE, (0.5 + self.end_y // co.TILE) * co.TILE

        x_tile, y_tile = x // co.TILE, y // co.TILE
        delta_x, delta_y = end_x - start_x, end_y - start_y
        distance = dist((end_x, start_x), (end_y, start_y))
        dx, dy = delta_x / distance, delta_y / distance
        x, y = start_x, start_y
        total_dy = 0
        s=set()
        while abs(total_dy) < abs(delta_y):
            total_dy += dy
            x += dx
            y += dy
            if (int(x // co.TILE), int(y // co.TILE)) == (x_tile, y_tile):
                return True
        return False
    
    def is_child(self, parent_root: 'Root'):
        root = self
        if root is parent_root:
            return True
        while root.parent is not None:
            root = root.parent
            if root is parent_root:
                return True
        return False


    def _update_texture(self):
        pass

    def increase_width(self):
        self.width += 1
        self._update_texture()

    def is_visible(self, current_height: int):
        bottom = self.y + self.texture_height - current_height
        return current_height + co.HEIGHT >= bottom or bottom >= 0


class RootGhost:
    def __init__(self) -> None:
        self.start_x: int = -1
        self.start_y: int = -1
        self.end_x: int = -1
        self.end_y: int = -1
        self.x: int = -1
        self.y: int = -1
        self.enabled: bool = False
        self.texture: Surface = None
        self.texture_ready: bool = False
        self.correct: bool = False
        self.starting_root: Root = None

    def enable(self, x: int, y: int, starting_root: Root):
        self.start_x = x
        self.start_y = y
        self.enabled = True
        self.correct = True
        self.starting_root = starting_root

    def disable(self):
        self.enabled = False
        self.texture_ready = False
        self.correct = False
        self.starting_root = None

    def get_length(self, mouse_x: int, mouse_y: int):
        return ((self.start_x - mouse_x) ** 2 + (self.start_y - mouse_y) ** 2) ** 0.5

    def set_endpoint(self, mouse_x: int, mouse_y: int):
        self.end_x = mouse_x
        self.end_y = mouse_y

        self.update_texture()

    def update_texture(self):
        if not self.enabled:
            return
        
        height = co.GHOST_ROOT_HEIGHT
        distance = dist((self.end_x, self.end_y), (self.start_x, self.start_y))
        angle = -atan2(self.end_y - self.start_y, self.end_x - self.start_x) # radians

        self.texture = Surface((distance, height), flags=pyg.SRCALPHA)
        pyg.draw.polygon(self.texture, (255, 255, 255, 255), ((0, 0), (distance, height / 2 - 1), (distance, height / 2 + 1), (0, height)))
        self.texture.blit(tx.BASE_ROOT if self.correct else tx.BASE_ROOT_RED, pyg.Rect(0, 0, distance, height), special_flags=pyg.BLEND_RGBA_MIN)
        self.texture = pyg.transform.rotate(self.texture, angle * 180 / pi)

        width, height = self.texture.get_width(), self.texture.get_height()
        self.x = self.start_x - width / 2 + distance / 2 * cos(angle)
        self.y = self.start_y - height / 2 - distance / 2 * sin(angle)
        
        self.texture_ready = True