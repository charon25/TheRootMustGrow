import pygame
import pyghelper

import constants as co

import random
random.seed(42)

pygame.init()
pygame.display.init()
screen = pyghelper.Window.create(width=co.WIDTH, height=co.HEIGHT, title='Global Game Jam 2023') #, icon_path='resources/icon.png')

from game import Game

pygame.init()

game = Game(screen)
game.start_game()

while not game.has_ended:
    game.loop()

game.stop()
