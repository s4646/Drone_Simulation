import cv2
import numpy as np
import math
from Point import Point

class Chopper(Point):
    def __init__(self, name):
        super(Chopper, self).__init__(name)
        self.icon = cv2.imread("pictures/drone.png") /255.0
        self.icon_w = 25
        self.icon_h = 25
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
        self.tips = []
        self.sensors = []

    def create_tips(self):
        # Convert angle to radians
        angle_rad = math.radians(self.angle)
        # Get x, y
        y, x = self.get_position()
        
        top_left = [y-self.icon_h/2, x-self.icon_w/2]
        top_left[0] = int(np.floor(top_left[1] * math.sin(angle_rad) + top_left[0] * math.cos(angle_rad)))
        top_left[1] = int(np.floor(top_left[1] * math.cos(angle_rad) - top_left[0] * math.sin(angle_rad)))
        
        top_right = [y-self.icon_h/2, x+self.icon_w/2]
        top_right[0] = int(np.floor(top_right[1] * math.sin(angle_rad) + top_right[0] * math.cos(angle_rad)))
        top_right[1] = int(np.floor(top_right[1] * math.cos(angle_rad) - top_right[0] * math.sin(angle_rad)))

        bottom_right = [(y+self.icon_h/2), (x+self.icon_w/2)]
        bottom_right[0] = int(np.floor(bottom_right[1] * math.sin(angle_rad) + bottom_right[0] * math.cos(angle_rad)))
        bottom_right[1] = int(np.floor(bottom_right[1] * math.cos(angle_rad) - bottom_right[0] * math.sin(angle_rad)))

        bottom_left = [(y+self.icon_h/2), (x-self.icon_w/2)]
        bottom_left[0] = int(np.floor(bottom_left[1] * math.sin(angle_rad) + bottom_left[0] * math.cos(angle_rad)))
        bottom_left[1] = int(np.floor(bottom_left[1] * math.cos(angle_rad) - bottom_left[0] * math.sin(angle_rad)))
        
        self.tips =  [top_left, top_right, bottom_right, bottom_left]

    def create_sensors(self):
        # Convert angle to radians
        angle_rad = math.radians(self.angle)
        # Get x, y
        y, x = self.get_position()

        top_sensor = [(y-self.icon_h-10), (x)]
        top_sensor[0] = int(np.floor(top_sensor[1] * math.sin(angle_rad) + top_sensor[0] * math.cos(angle_rad)))
        top_sensor[1] = int(np.floor(top_sensor[1] * math.cos(angle_rad) - top_sensor[0] * math.sin(angle_rad)))

        right_sensor = [(y), (x+self.icon_w+10)]
        right_sensor[0] = int(np.floor(right_sensor[1] * math.sin(angle_rad) + right_sensor[0] * math.cos(angle_rad)))
        right_sensor[1] = int(np.floor(right_sensor[1] * math.cos(angle_rad) - right_sensor[0] * math.sin(angle_rad)))

        bottom_sensor = [(y+self.icon_h+10), (x)]
        bottom_sensor[0] = int(np.floor(bottom_sensor[1] * math.sin(angle_rad) + bottom_sensor[0] * math.cos(angle_rad)))
        bottom_sensor[1] = int(np.floor(bottom_sensor[1] * math.cos(angle_rad) - bottom_sensor[0] * math.sin(angle_rad)))

        left_sensor = [y, x-self.icon_w-10]
        left_sensor[0] = int(np.floor(left_sensor[1] * math.sin(angle_rad) + left_sensor[0] * math.cos(angle_rad)))
        left_sensor[1] = int(np.floor(left_sensor[1] * math.cos(angle_rad) - left_sensor[0] * math.sin(angle_rad)))
        
        self.sensors = [top_sensor, right_sensor, bottom_sensor, left_sensor]
    
    def rotate_icon(self):
        self.icon = cv2.imread("pictures/drone.png") /255.0
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))

        # Create the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((self.icon_w//2, self.icon_h//2), self.angle, 1.0)

        # Apply the rotation
        rotated_image = cv2.warpAffine(self.icon, rot_mat, (self.icon.shape[1], self.icon.shape[0]))

        self.icon = rotated_image