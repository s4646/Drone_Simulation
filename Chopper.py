import cv2
import math
import numpy as np
from numba import njit
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
        self.visited = np.empty((0, 2))

    def create_tips(self):
        y, x = self.get_position()
        angle_rad = math.radians(self.angle)

        top_left_coord = y-self.icon_h//2, x-self.icon_w//2
        top_left = self.rotate((y,x), top_left_coord, angle_rad)

        top_right_coord = y-self.icon_h//2, x+self.icon_w//2
        top_right = self.rotate((y,x), top_right_coord, angle_rad)

        bottom_right_coord = y+self.icon_h//2, x+self.icon_w//2
        bottom_right = self.rotate((y,x), bottom_right_coord, angle_rad)

        bottom_left_coord = y+self.icon_h//2, x-self.icon_w//2
        bottom_left = self.rotate((y,x), bottom_left_coord, angle_rad)
        
        self.tips =  [top_left, top_right, bottom_right, bottom_left]
        print(self.tips)

    def create_sensors(self, pitch, roll):
        y, x = self.get_position()
        angle_rad = math.radians(self.angle)
        north_sensor = int((y-self.icon_h-10) + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), int(x + math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        east_sensor = int(y + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), (x+self.icon_w+10) + int(math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        south_sensor = int((y+self.icon_h+10) + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), x + int(math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        west_sensor = int(y + math.sin(angle_rad) * pitch + math.cos(angle_rad) * roll), (x-self.icon_w-10) + int(math.cos(angle_rad) * pitch + math.sin(angle_rad) * roll)
        
        self.sensors = [north_sensor, east_sensor, south_sensor, west_sensor]
        
        temp = self.interpolate_pixels_along_line(north_sensor[1], north_sensor[0], south_sensor[1], south_sensor[0])
        self.visited = np.concatenate([self.visited, temp])

        temp = self.interpolate_pixels_along_line(east_sensor[1], east_sensor[0], west_sensor[1], west_sensor[0])
        self.visited = np.concatenate([self.visited, temp])

        self.visited = np.unique(self.visited, axis=0)
        # print(self.sensors)
    
    def rotate_icon(self):
        h, w = self.icon_h, self.icon_w
        center = (w // 2, h // 2)
        rot_mat = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        return cv2.warpAffine(self.icon, rot_mat, (w, h), flags=cv2.INTER_CUBIC, borderMode = cv2.BORDER_CONSTANT, borderValue=[255, 255, 255])

    @staticmethod
    @njit
    def interpolate_pixels_along_line(x0, y0, x1, y1):
        """
        Uses Xiaolin Wu's line algorithm to interpolate all of the pixels along a straight line,
        given two points (x0, y0) and (x1, y1).
        """
        pixels = []
        steep = abs(y1 - y0) > abs(x1 - x0)

        # Ensure that the path to be interpolated is shallow and from left to right
        if steep:
            t = x0
            x0 = y0
            y0 = t
            t = x1
            x1 = y1
            y1 = t

        if x0 > x1:
            t = x0
            x0 = x1
            x1 = t
            t = y0
            y0 = y1
            y1 = t

        dx = x1 - x0
        dy = y1 - y0
        gradient = dy / dx  # slope

        # Get the first given coordinate and add it to the return list
        x_end = round(x0)
        y_end = y0 + (gradient * (x_end - x0))
        xpxl0 = x_end
        ypxl0 = round(y_end)

        if steep:
            pixels.extend([(xpxl0, ypxl0), (xpxl0, ypxl0 + 1)])
        else:
            pixels.extend([(ypxl0, xpxl0), (ypxl0 + 1, xpxl0)])

        interpolated_y = y_end + gradient

        # Get the second given coordinate to give the main loop a range
        x_end = round(x1)
        y_end = y1 + (gradient * (x_end - x1))
        xpxl1 = x_end
        ypxl1 = round(y_end)

        # Loop between the first x coordinate and the second x coordinate,
        # interpolating the y coordinates
        for x in range(xpxl0 + 1, xpxl1):
            if steep:
                pixels.extend([(x, math.floor(interpolated_y)), (x, math.floor(interpolated_y) + 1)])
            else:
                pixels.extend([(math.floor(interpolated_y), x), (math.floor(interpolated_y) + 1, x)])
            interpolated_y += gradient

        # Add the second given coordinate to the list
        if steep:
            pixels.extend([(xpxl1, ypxl1), (xpxl1, ypxl1 + 1)])
        else:
            pixels.extend([(ypxl1, xpxl1), (ypxl1 + 1, xpxl1)])

        return np.array(pixels, dtype=np.uint16)