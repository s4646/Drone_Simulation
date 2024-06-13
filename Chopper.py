import cv2
import math
import numpy as np
from numba import njit
from Point import Point

class Chopper(Point):
    def __init__(self, name):
        super(Chopper, self).__init__(name)
        self.icon = cv2.imread("pictures/drone.png") / 255.0
        
        self.angle = -90
        self.start_point = None
        
        
        self.icon_w = 8
        self.icon_h = 8
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

    def create_sensors(self):
        y, x = self.get_position()
        angle_rad = math.radians(self.angle)

        top_sensor_coord = y-self.icon_h-32, x
        top_sensor = self.rotate((y,x), top_sensor_coord, angle_rad) 

        right_sensor_coord = y, x+self.icon_w+32
        right_sensor = self.rotate((y,x), right_sensor_coord, angle_rad)

        bottom_sensor_coord = y+self.icon_h+32, x
        bottom_sensor = self.rotate((y,x), bottom_sensor_coord, angle_rad)

        left_sensor_coord = y, x-self.icon_w-32
        left_sensor = self.rotate((y,x), left_sensor_coord, angle_rad)
        
        self.sensors = [top_sensor, right_sensor, bottom_sensor, left_sensor]
    
    def rotate_icon(self):
        h, w = self.icon_h, self.icon_w
        center = (w // 2, h // 2)
        rot_mat = cv2.getRotationMatrix2D(center, -self.angle, 1.0)
        return cv2.warpAffine(self.icon, rot_mat, (w, h), flags=cv2.INTER_CUBIC, borderMode = cv2.BORDER_CONSTANT, borderValue=[255, 255, 255])

    @staticmethod
    @njit
    def interpolate_pixels_along_line(y0, x0, y1, x1):
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