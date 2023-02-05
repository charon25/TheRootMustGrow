import pygame
import pyghelper

import constants as co

pygame.init()
pygame.display.init()
screen = pyghelper.Window.create(width=co.WIDTH, height=co.HEIGHT, title='The Root Must Grow') #, icon_path='resources/icon.png')

from game import Game

pygame.init()

game = Game(screen)

while not game.has_ended:
    game.loop()

game.stop()
