import cv2
from Point import Point

class Chopper(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(Chopper, self).__init__(name, x_max, x_min, y_max, y_min)
        self.icon = cv2.imread("pictures/drone.png") /255.0
        self.icon_w = 32
        self.icon_h = 32
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))

    
# class Bird(Point):
#     def __init__(self, name, x_max, x_min, y_max, y_min):
#         super(Bird, self).__init__(name, x_max, x_min, y_max, y_min)
#         self.icon = cv2.imread("bird.png") / 255.0
#         self.icon_w = 32
#         self.icon_h = 32
#         self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
    
# class Fuel(Point):
#     def __init__(self, name, x_max, x_min, y_max, y_min):
#         super(Fuel, self).__init__(name, x_max, x_min, y_max, y_min)
#         self.icon = cv2.imread("fuel.png") / 255.0
#         self.icon_w = 32
#         self.icon_h = 32
#         self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))