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

    def get_point_by_distance(self, angle: float, distance: float):
        angle_rad = np.deg2rad(angle)
        i = distance
        
        y = self.y + i*np.sin(angle_rad)
        x = self.x + i*np.cos(angle_rad)

        return y, x

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