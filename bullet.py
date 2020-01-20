from base_object import BaseObject
import math
import numpy as np
import utils
import config


class Bullet(BaseObject):
    def __init__(self, x, y, angle, vx, vy):
        vx += config.bullet_speed*math.cos(math.radians(angle))
        vy += config.bullet_speed*math.sin(math.radians(angle))
        self.creation = utils.get_now()
        super().__init__(x, y, vx, vy, img=255 * np.ones((3, 3, 3), dtype="uint8"))

    def remove(self):
        return utils.it_is_time(self.creation, config.bullet_lifetime)
