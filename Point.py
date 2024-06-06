import math

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
    
    def pitch(self, dir=True):
        p = 1 if dir else -1
        self.x += math.cos(math.radians(self.angle)) * p
        self.y += math.sin(math.radians(self.angle)) * p

    def roll(self, dir=True):
        r = 1 if dir else -1
        self.x += math.sin(math.radians(self.angle)) * r
        self.y += math.cos(math.radians(self.angle)) * r
    
    def yaw(self, dir=True):
        y = 1 if dir else -1
        self.angle += y