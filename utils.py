from math import ceil, cos, pi, sin
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

def generate_circular_pos_velocity_in_disk(disk_radius: float, x_center: float, y_center: float):#, vx: float, vy: float) -> tuple[float, float, float, float]:
    radius = disk_radius * random()
    angle = random() * 2 * pi

    return (
        x_center + radius * cos(angle),
        y_center + radius * sin(angle),
        cos(angle),
        sin(angle)
    )

def random_sym_float(amplitude: float):
    return 2 * random() * amplitude - amplitude

def get_resource_string(quantity: float, divisor: int, letter: str, after_comma: int = 1) -> str:
    q, r = quantity // divisor, quantity % divisor
    r = round(r / (divisor // (10 ** after_comma)), 0)

    if q > 1000:
        return f'999{letter}'
    if q > 10 or r == 0:
        return f'{q:.0f}{letter}'
    return f'{q:.0f}{letter}{r:.0f}'

def int_to_small_string(value: int, after_comma: int = 1, apply_ceil: bool = False) -> str:
    if 1_000 > value >= 0:
        if apply_ceil:
            return f'{ceil(value):.{after_comma - 1}f}'
        else:
            return f'{value:.{after_comma - 1}f}'
    elif 1_000_000 > value >= 1_000:
        return get_resource_string(value, 1_000, 'K', after_comma)
    elif 1_000_000_000 > value >= 1_000_000:
        return get_resource_string(value, 1_000_000, 'M', after_comma)
    elif value >= 1_000_000_000:
        return get_resource_string(value, 1_000_000_000, 'B', after_comma)

def random_float(min: float, max: float):
    return random() * (max - min) + min

def void(*args):
    pass

def point_in_rectangle(x: int, y: int, left: int, top: int, width: int, height: int):
    return left <= x <= left + width and top <= y <= top + height
