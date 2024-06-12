import cv2 
import time
import math
import random
import numpy as np 
from Map import Map
from numba import njit
from Chopper import Chopper
from collections import namedtuple
from ChopperController import ChopperController

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

class Environment(object):
    def __init__(self, path: str) -> None:
        # Define environment space
        self.map = Map(path)
        self.observation_shape = self.map.map.shape

        # Define chopper
        self.chopper = Chopper("chopper")
        self.controller = ChopperController()

        self.velocity = namedtuple('Velocity', ('vX', 'vY'))
        self.acceleration = namedtuple('Acceleration', ('accX', 'accY'))
        self.max_fuel = 4800


        # Create a canvas to render the environment images upon 
        self.canvas = np.ones(self.observation_shape) * 1

        # Permissible area of chopper to be 
        self.y_min = int (self.observation_shape[0] * 0.1)
        self.x_min = 0
        self.y_max = int (self.observation_shape[0] * 0.9)
        self.x_max = self.observation_shape[1]
        
    @staticmethod
    @njit
    def draw_map_on_canvas(canvas: np.ndarray, map: np.ndarray):
        # Init the canvas 
        canvas = np.ones(map.shape) * 1
        
        h, w, _ = canvas.shape
        for y in range(h):
            for x in range(w):
                canvas[y, x] = map[y, x]
        
        return canvas
    
    def draw_chopper_on_canvas(self):
        # Init the canvas 
        # self.canvas = np.ones(self.observation_shape) * 1

        # Draw the heliopter on canvas
        chopper_shape = self.chopper.icon.shape
        y, x = self.chopper.y, self.chopper.x
        self.canvas[int(y - chopper_shape[1]/2) : int(y + chopper_shape[1]/2), int(x - chopper_shape[0]/2 ): int(x + chopper_shape[0]/2)] = self.chopper.rotate_icon()

        text = 'Fuel Left: {}'.format(self.fuel_left)

        # Put the info on canvas 
        self.canvas = cv2.putText(self.canvas, text, (10,20), font,  
                0.8, (255,255,0), 1, cv2.LINE_AA)
     
    def render(self, mode = "human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            cv2.imshow("Simulation", self.canvas)
            cv2.waitKey(100)
        
        elif mode == "rgb_array":
            return self.canvas
        
    def close(self):
        cv2.destroyAllWindows()
        
    def has_collided(self):
        tips = self.chopper.tips
        if self.map.is_black(tips[0][0], tips[0][1]): return True
        elif self.map.is_black(tips[1][0], tips[1][1]): return True
        elif self.map.is_black(tips[2][0], tips[2][1]): return True
        elif self.map.is_black(tips[3][0], tips[3][1]): return True
        else: return False

    def scan_area(self):
        ch = self.chopper
        danger_meter = [0, 0, 0, 0] # how close each sensor is to a wall

        temp = ch.interpolate_pixels_along_line(ch.sensors[0][0], ch.sensors[0][1], ch.sensors[2][0], ch.sensors[2][1])
        for i, point in enumerate(temp):
            if self.map.is_black(point[0], point[1]):
                # Count danger                
                dist_top = np.sqrt((ch.sensors[0][0] - point[0]) ** 2) + np.sqrt((ch.sensors[0][1] - point[1]) ** 2)
                dist_bottom = np.sqrt((ch.sensors[2][0] - point[0]) ** 2) + np.sqrt((ch.sensors[2][1] - point[1]) ** 2)
                if dist_top < dist_bottom: danger_meter[0] += 1
                else: danger_meter[2] += 1
                
                # Delete black point from visited
                try: temp = np.delete(temp, i, axis=0)
                except IndexError: continue
        
        ch.visited = np.concatenate([ch.visited, temp])

        temp = ch.interpolate_pixels_along_line(ch.sensors[1][0], ch.sensors[1][1], ch.sensors[3][0], ch.sensors[3][1])
        for i, point in enumerate(temp):
            if self.map.is_black(point[0], point[1]):
                # Count danger
                dist_right = np.sqrt((ch.sensors[1][0] - point[0]) ** 2) + np.sqrt((ch.sensors[1][1] - point[1]) ** 2)
                dist_left = np.sqrt((ch.sensors[3][0] - point[0]) ** 2) + np.sqrt((ch.sensors[3][1] - point[1]) ** 2)
                if dist_right < dist_left: danger_meter[1] += 1
                else: danger_meter[3] += 1

                # Delete black point from visited
                try: temp = np.delete(temp, i, axis=0)
                except IndexError: continue

        ch.visited = np.concatenate([ch.visited, temp])

        ch.visited = np.unique(ch.visited, axis=0)
        return danger_meter
    
    def reset(self):
        # Reset the fuel consumed
        self.fuel_left = self.max_fuel
        # Reset scanned area (visited pixels)
        self.total_visited = 0

        # Determine a place to intialise the chopper in
        x = 700 # 100
        y = 400 # 80

        # Intialise the chopper
        self.chopper = Chopper("chopper")
        self.chopper.set_position(y, x)
        self.chopper.create_tips()
        self.chopper.create_sensors()

        # Reset the Canvas 
        self.canvas = np.ones(self.observation_shape) * 1
        
        return False

    def step(self):
        # Flag that marks the termination of an episode
        done = False

        # Scan area and check collision danger meter
        danger_meter = self.scan_area()
        # print(f"danger meter: {danger_meter}")

        # Take action
        p, r = 0, 0
        ###
        # IMPLEMENT ALGORITHM HERE
        ###
        
        # print(f"desired: {p}, {r}, {y}")
        p, r = self.controller.update(p, self.chopper.pitch, r, self.chopper.roll)
        # print(f"actual: {p}, r: {r}, y: {y}")

        self.chopper.set_pitch_roll_yaw(p, r, y)
        self.chopper.move()
        self.chopper.create_tips()
        self.chopper.create_sensors()

        # Decrease the fuel counter 
        self.fuel_left -= 1      

        # Draw elements on the canvas
        self.canvas = self.draw_map_on_canvas(self.canvas, self.map.map)      
        for coord in self.chopper.visited:
            y, x = coord
            x = int(round(x))
            y = int(round(y))
            if not self.map.is_black(y, x): self.canvas[y, x] = [255, 0, 0]
        self.draw_chopper_on_canvas()
        for tip in self.chopper.tips:
            y, x = tip
            x = int(round(x))
            y = int(round(y))
            if not self.map.is_black(y, x): self.canvas[y, x] = [0, 0, 255]
        
        # Conclude the episode
        if self.has_collided(): done = True # If chopper has collided, end the episode       
        if self.fuel_left == 0: done = True # If out of fuel, end the episode.

        # print(f"Pitch: {self.pitch}, Roll: {self.roll}, Yaw: {self.yaw}")
        # print(f"Position: {self.chopper.y}, {self.chopper.x}")
        return done