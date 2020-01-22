from simulation import Simulation
from crappyAI import RandomDevil
import config
import matplotlib.image
import os

def collect(agent, folder, num_images):
    if not os.path.exists(folder):
        os.makedirs(folder)
    saved_images = 0
    framecounter = 0
    config.DRAW = False
    config.RENDER = False
    config.use_ticks = True
    sim = Simulation()
    score = 0
    while saved_images < num_images:
        framecounter += 1
        key = agent.react(sim)
        if framecounter >= config.fps / 10:
            framecounter = 0
            config.DRAW = True
            ret = sim.step(key)
            config.DRAW = False
            matplotlib.image.imsave(f"{folder}/run_frame_{saved_images}.png", ret[0])
            print(f"saved image {saved_images}")
            saved_images += 1
            score = 0
        else:
            ret = sim.step(key)
        score += ret[1]
        if ret[2]:
            sim.reset()
            framecounter = 0
            score = 0
            continue


if __name__ == "__main__":
    config.fps = 30
    ai = RandomDevil(Simulation.action_space, pause=6)
    collect(ai, "data", 10000)