from math import atan2, cos, dist, pi, sin

import pygame as pyg
from pygame import Surface

import constants as co
import textures as tx


class Root:
    def __init__(self, x: int, y: int, texture: Surface) -> None:
        self.x: int = x
        self.y: int = y
        self.texture: Surface = texture
        self.texture_height = self.texture.get_height()
        self.width: int = 1

    def _update_texture(self):
        pass

    def increase_width(self):
        self.width += 1
        self._update_texture()

    def is_visible(self, current_height: int):
        return current_height + co.HEIGHT >= self.y + self.texture_height - current_height >= 0


class RootGhost:
    def __init__(self) -> None:
        self.start_x: int = -1
        self.start_y: int = -1
        self.x: int = -1
        self.y: int = -1
        self.enabled: bool = False
        self.texture: Surface = None
        self.texture_ready: bool = False

    def enable(self, x: int, y: int):
        self.start_x = x
        self.start_y = y
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.texture_ready = False

    def update_texture(self, mouse_x: int, mouse_y: int):
        if not self.enabled:
            return
        
        height = co.GHOST_ROOT_HEIGHT
        distance = dist((mouse_x, mouse_y), (self.start_x, self.start_y))
        angle = -atan2(mouse_y - self.start_y, mouse_x - self.start_x) # radians

        self.texture = Surface((distance, height), flags=pyg.SRCALPHA)
        pyg.draw.polygon(self.texture, (255, 255, 255, 255), ((0, 0), (distance, height / 2 - 1), (distance, height / 2 + 1), (0, height)))
        self.texture.blit(tx.BASE_ROOT, pyg.Rect(0, 0, distance, height), special_flags=pyg.BLEND_RGBA_MIN)
        self.texture = pyg.transform.rotate(self.texture, angle * 180 / pi)

        width, height = self.texture.get_width(), self.texture.get_height()
        self.x = self.start_x - width / 2 + distance / 2 * cos(angle)
        self.y = self.start_y - height / 2 - distance / 2 * sin(angle)
        
        self.texture_ready = True
