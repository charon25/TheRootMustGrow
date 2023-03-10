from random import choice, randint, random

import constants as co
import textures as tx
import utils

from tile import TileType


def get_texture(type: TileType):
    if type == TileType.WATER:
        return choice(tx.WATER_PARTICLES)

    if type == TileType.NITROGEN:
        return choice(tx.NITROGEN_PARTICLES)

    if type == TileType.PHOSPHORUS:
        return choice(tx.PHOSPHORUS_PARTICLES)

    if 30 > type.value >= 20:
        return choice(tx.BONUS_PARTICLES)


class Particle:
    def __init__(self, x: int, y: int, vx: float, vy: float, type: TileType, fixed: bool = False) -> None:
        self.vx = vx
        self.vy = vy
        self.type = type
        self.texture = get_texture(self.type)
        self.half_height = self.texture.get_height() / 2
        self.x = x - self.half_height
        self.y = y - self.half_height
        self.life = co.PARTICLE_DURATION
        self.done = False
        self.is_fixed: bool = fixed

    def age(self):
        self.x += self.vx
        self.y += self.vy

        self.life -= 1
        if self.life <= 0:
            self.done = True

    def is_visible(self, current_height: int):
        return 0 <= self.y - current_height <= co.HEIGHT

    @classmethod
    def generate_extract_particle(cls, x: float, y: float, type: TileType, fixed: bool = False):
        if random() < co.EXTRACT_PARTICLE_PROBABILITY:
            return [
                Particle(
                    *utils.generate_pos_velocity_in_disk(
                        co.EXTRACT_PARTICLE_RADIUS,
                        x, y,
                        utils.random_sym_float(co.EXTRACT_PARTICLE_SPEED), utils.random_sym_float(co.EXTRACT_PARTICLE_SPEED)
                    ),
                    type,
                    fixed
                )
        ]
        else:
            return []

    @classmethod
    def generate_bonus_particles(cls, x: float, y: float, type: TileType):
        return [
            Particle(
                *utils.generate_circular_pos_velocity_in_disk(
                    co.TILE,
                    x, y
                ),
                type,
                False
            ) for count in range(co.BONUS_PARTICLES_COUNT)
        ]
