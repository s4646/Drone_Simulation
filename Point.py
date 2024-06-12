import math
import numpy as np
from numba import njit
class Point(object):
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.name = name
    
    def set_position(self, y, x):
        self.y = y
        self.x = x
    
    def get_position(self):
        return (self.y, self.x)

    def move(self, pitch, roll, angle):
            angle_rad = math.radians(angle)

            self.y += int(np.round(pitch * math.sin(angle_rad))) if math.sin(angle_rad) != 0 else pitch
            self.x += int(np.round(roll * math.cos(angle_rad))) if math.cos(angle_rad) != 0 else roll


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