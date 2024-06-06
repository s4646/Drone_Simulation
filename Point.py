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

    def move(self, pitch, roll , yaw):
        self.angle += yaw
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll
        self.y += math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll