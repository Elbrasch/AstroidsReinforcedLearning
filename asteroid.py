from base_object import BaseObject
import random


class Asteroid(BaseObject):
    def __init__(self, scale, x, y, vx, vy):
        self.scale = scale
        super().__init__(x, y, vx, vy, filename="asteroid.png", scale=scale, angle=0, rot=random.random() * 360)


    def split(self):
        if self.scale / 2. < 0.1:
            return []
        dv1 = 2 * random.random()
        dv2 = 2 * random.random()
        a1 = Asteroid(self.scale / 2., self.x + self.img.shape[1] / 2, self.y + self.img.shape[0] / 2,
                      self.vx * (1 + dv1),
                      self.vy * (1 + dv2))
        a2 = Asteroid(self.scale / 2., self.x - self.img.shape[1] / 2, self.y - self.img.shape[0] / 2,
                      self.vx * (1 - dv1),
                      self.vy * (1 - dv2))
        return [a1, a2]
