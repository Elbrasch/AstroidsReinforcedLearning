import random


class RotateShoot:
    def __init__(self, actionspace):
        self.rotate = True
        self.actionspace = actionspace

    def react(self, state):
        self.rotate = not self.rotate
        if self.rotate:
            return self.actionspace[2]
        else:
            return self.actionspace[5]


class RandomDevil:
    def __init__(self, actionspace, pause=1):
        self.actionspace = actionspace
        self.pause = pause
        self.tick_counter = 0

    def react(self, state):
        self.tick_counter += 1
        if self.tick_counter < self.pause:
            return -1
        self.tick_counter = 0
        return self.actionspace[random.randint(0, len(self.actionspace) - 1)]


if __name__ == "__main__":
    from simulation import Simulation
    import config
    import numpy as np

    config.DRAW = False
    config.RENDER = False
    config.use_ticks = True
    scores = []
    sim = Simulation()
    for i in range(100):
        ai = RandomDevil(sim.action_space)
        while True:
            key = ai.react(sim)
            ret = sim.step(key)
            if ret[2]:
                print("Score is ", sim.score)
                scores.append(ret)
                sim.reset()
                break
    print("Average score: ", np.array(scores).mean())
