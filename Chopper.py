import cv2
import math
import numpy as np
from Point import Point

class Chopper(Point):
    def __init__(self, name):
        super(Chopper, self).__init__(name)
        self.icon = cv2.imread("pictures/drone.png") /255.0
        self.icon_w = 12
        self.icon_h = 12
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
        self.tips = []
        self.sensors = []

    def create_tips(self, pitch, roll):
        y, x = self.get_position()
        angle_rad = math.radians(self.angle)
        top_left = int((y-self.icon_h//2) + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), int((x-self.icon_w//2) + math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        top_right = int((y-self.icon_h//2) + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), int((x+self.icon_w//2) + math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        bootom_right = int((y+self.icon_h//2) + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), int((x+self.icon_w//2) + math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        bottom_left = int((y+self.icon_h//2) + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), int((x-self.icon_w//2) + math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        
        self.tips =  [top_left, top_right, bootom_right, bottom_left]

    def create_sensors(self, pitch, roll):
        y, x = self.get_position()
        angle_rad = math.radians(self.angle)
        north_sensor = int((y-self.icon_h-10) + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), int(x + math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        east_sensor = int(y + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), (x+self.icon_w+10) + int(math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        south_sensor = int((y+self.icon_h+10) + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), x + int(math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        west_sensor = int(y + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), (x-self.icon_w-10) + int(math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        
        self.sensors = [north_sensor, east_sensor, south_sensor, west_sensor]
    
    def rotate_icon(self):
        h, w = self.icon_h, self.icon_w
        center = (w // 2, h // 2)
        rot_mat = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        return cv2.warpAffine(self.icon, rot_mat, (w, h), flags=cv2.INTER_CUBIC, borderMode = cv2.BORDER_CONSTANT, borderValue=[255, 255, 255])
