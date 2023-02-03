from math import atan2, cos, dist, pi, sin

import pygame as pyg
from pygame import Surface

import constants as co
import textures as tx


class Root:
    pass

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
        self.texture.blit(tx.BASE_ROOT, pyg.Rect(0, 0, distance, height))
        self.texture = pyg.transform.rotate(self.texture, angle * 180 / pi)

        width, height = self.texture.get_width(), self.texture.get_height()
        self.x = self.start_x - width / 2 + distance / 2 * cos(angle)
        self.y = self.start_y - height / 2 - distance / 2 * sin(angle)
        
        self.texture_ready = True
