import cv2
import imutils
import math
import config
from functools import lru_cache


@lru_cache()
def get_image(filename):
    return cv2.imread(filename)


class BaseObject:
    def __init__(self, x, y, vx, vy, filename=None, rot=0, scale=None, angle=None, img=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.rot = rot
        if filename is not None:
            assert angle is not None
            assert scale is not None
            self.img = get_image(filename)
            self.img = imutils.rotate(self.img, angle=angle)
            width = int(self.img.shape[1] * scale)
            height = int(self.img.shape[0] * scale)
            self.img = cv2.resize(self.img, (width, height))
            assert img is None
        elif img is not None:
            self.img = img
        else:
            raise Exception("No filename or image defined")

    def move(self):
        self.x += (60 / config.fps) * self.vx
        self.y += (60 / config.fps) * self.vy

    def distance(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def check_bondary(self, img):
        if self.x <= 0:
            self.x = img.shape[1] - self.img.shape[1]
        if self.x + self.img.shape[1] > img.shape[1]:
            self.x = 0
        if self.y <= 0:
            self.y = img.shape[0] - self.img.shape[0]
        if self.y + self.img.shape[0] > img.shape[0]:
            self.y = 0

    def draw(self, img):
        if not config.DRAW:
            return img
        x = int(self.x)
        y = int(self.y)
        img[y:y + self.img.shape[0], x:x + self.img.shape[1]] = imutils.rotate(self.img, angle=-self.rot)
        return img

    def check_crash(self, other):
        dist = other.distance(self.x, self.y)
        return 2 * dist < max(self.img.shape[:2]) + max(other.img.shape[:2])

    def tick(self, frame):
        self.move()
        self.check_bondary(frame)
        return self.draw(frame)
