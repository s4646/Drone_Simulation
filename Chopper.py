import cv2
from Point import Point

class Chopper(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(Chopper, self).__init__(name, x_max, x_min, y_max, y_min)
        self.icon = cv2.imread("pictures/drone.png") /255.0
        self.icon_w = 32
        self.icon_h = 32
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
        self.tips = self.create_tips()
        self.sensors = self.create_sensors()

    def create_tips(self):
        x, y = self.get_position()
        top_left = x-self.icon_w/2, y-self.icon_h/2
        top_right = x+self.icon_w/2, y-self.icon_h/2
        bootom_right = x+self.icon_w/2, y+self.icon_h/2
        bottom_left = x-self.icon_w/2, y+self.icon_h/2
        
        return [top_left, top_right, bootom_right, bottom_left]

    def create_sensors(self):
        x, y = self.get_position()
        north_sensor = x, y-self.icon_h-10
        east_sensor = x+self.icon_w+10, y
        south_sensor = x, y+self.icon_h+10
        west_sensor = x-self.icon_w-10, y
        
        return [north_sensor, east_sensor, south_sensor, west_sensor]