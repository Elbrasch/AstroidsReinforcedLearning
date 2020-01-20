import math
from base_object import BaseObject
from bullet import Bullet
import config
import utils


class Spaceship(BaseObject):
    def __init__(self, scale, speed, rotationspeed):
        super().__init__(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2, 0, 0, filename="A10.png", scale=scale, angle=90)
        self.rotationspeed = rotationspeed
        self.speed = speed
        self.last_shot = utils.get_now()

    def boost(self, kick):
        self.vx += kick * math.cos(math.radians(self.rot))
        self.vy += kick * math.sin(math.radians(self.rot))

    def remove(self):
        return False

    def shoot(self):
        if utils.it_is_time(self.last_shot, config.bullet_cooldown):
            self.last_shot = utils.get_now()
            return [Bullet(self.x + self.img.shape[1] / 2, self.y + self.img.shape[0] / 2, self.rot, self.vx, self.vy)]
        else:
            return []

    def update_velocity(self, key):
        if key == 119:
            self.boost(self.speed)
        elif key == 97:
            self.rot -= self.rotationspeed
        elif key == 115:
            self.boost(-self.speed)
        elif key == 100:
            self.rot += self.rotationspeed

    def check_bondary(self, img):
        super().check_bondary(img)
        self.rot = self.rot % 360

    def tick(self, key, frame):
        self.update_velocity(key)
        return super().tick(frame)
