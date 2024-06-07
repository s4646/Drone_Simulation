import math
import numpy as np
from numba import njit
class Point(object):
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.name = name
    
    def set_position(self, y, x):
        self.y = y
        self.x = x
    
    def get_position(self):
        return (self.y, self.x)

    def move(self, pitch, roll , yaw):
        self.angle += yaw
        angle_rad = math.radians(self.angle)
        self.y += math.floor((math.sin(angle_rad) + math.cos(angle_rad)) * pitch) 
        self.x += math.floor((math.cos(angle_rad) + math.sin(angle_rad)) * roll)

    @staticmethod
    @njit
    def rotate(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.
        The angle should be given in radians.
        """
        oy, ox = origin
        py, px = point
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy) 
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        return math.floor(qy), math.floor(qx)