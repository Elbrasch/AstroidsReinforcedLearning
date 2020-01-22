import cv2
from asteroid import Asteroid
import random
import numpy as np
from spaceship import Spaceship
import config
import utils
from gym import Env


class Simulation(Env):
    action_space = [0, 119, 97, 115, 100, 32]

    def __init__(self):
        self.reset()

    def reset(self):
        self.ship = Spaceship(scale=.3, speed=0.06, rotationspeed=10)
        self.asteroids = []
        self.bullets = []
        self.frame = np.zeros((config.SCREEN_HEIGHT, config.SCREEN_WIDTH, 3), dtype="uint8")
        self.last_astroid = utils.get_now()
        self.now = utils.get_now()
        self.score = 0
        self.stars = []
        self.add_stars()

    def add_stars(self):
        for i in range(100):
            x = random.randint(1, config.SCREEN_WIDTH - 2)
            y = random.randint(1, config.SCREEN_HEIGHT - 2)
            brightness = random.randint(120, 255)
            self.stars.append((x, y, brightness))

    def draw_stars(self):
        for x, y, brightness in self.stars:
            self.frame[y, x - 1:x + 1] = int(brightness * 0.5)
            self.frame[y - 1:y + 1, x] = int(brightness * 0.5)
            self.frame[y, x] = brightness

    def run(self):
        assert config.DRAW
        while True:
            key = cv2.waitKey(1)
            if key == 27:
                return self.score
            r = self.step(key)
            if r[2]:
                print("Your score is ", self.score)
                cv2.destroyAllWindows()
                return r

    def step(self, action):
        reward = 0.0
        done = False
        if action == 32:
            self.bullets += self.ship.shoot()
        if config.DRAW:
            self.frame.fill(0)
            self.draw_stars()
        self.ship.tick(action, self.frame)
        for asteroid in self.asteroids:
            self.frame = asteroid.tick(self.frame)
            if self.ship.check_crash(asteroid):
                done = True
            for bullet in self.bullets:
                if bullet.check_crash(asteroid):
                    self.score += 1
                    reward += 1.
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    new_asteroids = asteroid.split()
                    self.asteroids += new_asteroids
        for bullet in self.bullets:
            self.frame = bullet.tick(self.frame)
            if bullet.remove():
                self.bullets.remove(bullet)
        if config.RENDER:
            cv2.imshow("space", self.frame)
            cv2.waitKey(1)

        if utils.it_is_time(self.last_astroid, config.asteroid_interval):
            ast = Asteroid(random.random() * 0.3 + 0.1, random.random() * config.SCREEN_WIDTH,
                           random.random() * config.SCREEN_HEIGHT,
                           (1 - random.random()) * 1.6,
                           (1 - random.random()) * 1.6)
            self.asteroids.append(ast)
            self.last_astroid = utils.get_now()
        self.now = utils.tick_time(self.now)
        return self.frame, reward, done, {}
