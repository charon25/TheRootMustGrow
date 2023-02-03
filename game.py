import pygame
from pygame import Surface
import pyghelper

import constants as co


class Game:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.has_ended = False

    def start(self) -> None:
        pass


    def loop(self) -> None:
        pass

    def stop(self) -> None:
        pass
