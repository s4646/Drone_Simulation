import gym
import cv2 
import time
import random
import numpy as np 
from Map import Map
import PIL.Image as Image
from gym import Env, spaces
from Chopper import Chopper
import matplotlib.pyplot as plt

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

class ChopperScape(Env):
    def __init__(self, path: str):
        super(ChopperScape, self).__init__()

        self.map = Map(path)
        
        # Define a 2-D observation space
        self.observation_shape = self.map.map.shape # (600, 800, 3)
        self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
                                            high = np.ones(self.observation_shape),
                                            dtype = np.float16)
        
        # Define an action space ranging from 0 to 4
        self.action_space = spaces.Discrete(6,)
                        
        # Create a canvas to render the environment images upon 
        self.canvas = np.ones(self.observation_shape) * 1
        
        # Define elements present inside the environment
        self.elements = []
        
        # Maximum fuel chopper can take at once
        self.max_fuel = 1000

        # Permissible area of helicper to be 
        self.y_min = int (self.observation_shape[0] * 0.1)
        self.x_min = 0
        self.y_max = int (self.observation_shape[0] * 0.9)
        self.x_max = self.observation_shape[1]

    def draw_elements_on_canvas(self):
        # Init the canvas 
        # self.canvas = np.ones(self.observation_shape) * 1

        # Draw the heliopter on canvas
        for elem in self.elements:
            elem_shape = elem.icon.shape
            x,y = elem.x, elem.y
            self.canvas[y : y + elem_shape[1], x:x + elem_shape[0]] = elem.icon

        text = 'Fuel Left: {} | Rewards: {}'.format(self.fuel_left, self.ep_return)

        # Put the info on canvas 
        self.canvas = cv2.putText(self.canvas, text, (10,20), font,  
                0.8, (255,255,0), 1, cv2.LINE_AA)
        
    def draw_map_on_canvas(self):
        # Init the canvas 
        self.canvas = np.ones(self.observation_shape) * 1
        
        w, h, _ = self.canvas.shape
        for x in range(w):
            for y in range(h):
                self.canvas[x, y] = self.map.map[x, y]

    def reset(self):
        # Reset the fuel consumed
        self.fuel_left = self.max_fuel

        # Reset the reward
        self.ep_return  = 0

        # Number of birds
        self.bird_count = 0
        self.fuel_count = 0

        # Determine a place to intialise the chopper in
        # x = random.randrange(int(self.observation_shape[0] * 0.05), int(self.observation_shape[0] * 0.10))
        # y = random.randrange(int(self.observation_shape[1] * 0.15), int(self.observation_shape[1] * 0.20))
        x = 100
        y = 50
        
        # Intialise the chopper
        self.chopper = Chopper("chopper", self.x_max, self.x_min, self.y_max, self.y_min)
        self.chopper.set_position(x,y)

        # Intialise the elements 
        self.elements = [self.chopper]

        # Reset the Canvas 
        self.canvas = np.ones(self.observation_shape) * 1

        # Draw elements on the canvas
        self.draw_map_on_canvas()
        self.draw_elements_on_canvas()

        # return the observation
        return self.canvas
    
if __name__ == "__main__":
    path_to_image = "pictures/maps/p11.png"
    env = ChopperScape(path_to_image)
    obs = env.reset()
    plt.imshow(obs)
    plt.show()