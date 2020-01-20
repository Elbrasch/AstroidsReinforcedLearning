import random

keys = [0, 119, 97, 115, 100, 32]


class RotateShoot:
    def __init__(self):
        self.rotate = True

    def react(self, state):
        if self.rotate:
            self.rotate = False
            return keys[2]
        else:
            self.rotate = True
            return keys[5]


class RandomDevil:
    def react(self, state):
        return keys[random.randint(0, len(keys) - 1)]


if __name__ == "__main__":
    from simulation import Simulation
    import config
    import numpy as np

    config.DRAW = False
    config.use_ticks = True
    scores = []
    sim = Simulation()
    for i in range(100):
        ai = RandomDevil()
        while True:
            key = ai.react(sim)
            ret = sim.step(key)
            if ret[2]:
                print("Score is ", sim.score)
                scores.append(ret)
                sim.reset()
                break
    print("Average score: ", np.array(scores).mean())
