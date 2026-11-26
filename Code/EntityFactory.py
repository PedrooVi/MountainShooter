import random

from Code.Assets import zombie_frames, zombie_height, zombie_names
from Code.Const import AIR_LIFT, GROUND_Y, WIN_WIDTH
from Code.Obstacle import Obstacle
from Code.Player import Player
from Code.Zombie import Zombie


class EntityFactory:
    @staticmethod
    def create_player(character_name):
        return Player(character_name)

    @staticmethod
    def create_zombie(kind):
        variant = random.choice(zombie_names())
        action = "run" if kind == "ground" else "jump"
        frames = zombie_frames(variant, action, zombie_height(kind))
        bottom = GROUND_Y if kind == "ground" else GROUND_Y - AIR_LIFT
        zombie = Zombie(kind, frames, bottom)
        zombie.rect.left = WIN_WIDTH + 20
        zombie.rect.bottom = bottom
        return zombie

    @staticmethod
    def create_obstacle():
        return Obstacle(WIN_WIDTH + 20)
