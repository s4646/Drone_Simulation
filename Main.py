import numpy as np
from Environment import Environment

def main():
    path_to_map = "pictures/maps/test.png"
    env = Environment(path_to_map)

    done = env.reset()
    while not done:

        # Simulation step
        done = env.step()

        # Render simulation
        env.render(mode='human')
        env.canvas = np.ones(env.observation_shape) * 1
    
    env.close()

if __name__ == "__main__":
    main()