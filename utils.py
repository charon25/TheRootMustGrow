from math import cos, pi, sin
from random import random

import pygame as pyg

import constants as co


def floor_n(x: int, n: int) -> int:
    return (x // n) * n

def get_font(size, bold=False, italic=False, underline=False):
    try:
        font = pyg.font.Font(co.FONT_PATH, size)
    except:
        font = pyg.font.SysFont("arial", size)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    return font

def clamped_lerp(x: float, min_x: float, max_x: float, min_y: float, max_y: float) -> float:
    if x < min_x:
        return min_y
    if x > max_x:
        return max_y

    return (x - min_x) / (max_x - min_x) * (max_y - min_y) + min_y

def generate_pos_velocity_in_disk(disk_radius: float, x_center: float, y_center: float, vx: float, vy: float) -> tuple[float, float, float, float]:
    radius = disk_radius * random()
    angle = random() * 2 * pi

    return (
        x_center + radius * cos(angle),
        y_center + radius * sin(angle),
        vx * cos(angle),
        vy * sin(angle)
    )

def random_sym_float(amplitude: float):
    return 2 * random() * amplitude - amplitude
