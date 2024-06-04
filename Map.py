import os
import numpy as np
from PIL import Image
from Point import Point
import matplotlib.pyplot as plt

class Map:
    def __init__(self, path): # , drone_start_point):
        # self.drone_start_point: tuple = drone_start_point
        self.img: Image = Image.open(path).convert('RGB')
        self.map: np.ndarray = self.render_map_from_image_to_boolean().transpose(1,0,2)
        self.point_map: np.ndarray = self.create_point_map()

    def render_map_from_image_to_boolean(self):
        w, h = self.img.size
        map_array = np.zeros((w, h, 3), dtype=int)
        for x in range(w):
            for y in range(h):
                coordinate = x, y
                r, g, b = self.img.getpixel(coordinate)
                if r != 0 and g != 0 and b != 0:  # consider black
                    map_array[x, y , :] = 255
        return map_array

    def is_collide(self, x, y):
        return not self.map[x, y]

    def create_point_map(self):
        w, h, _ = self.map.shape
        point_map = np.ndarray((w, h))
        for x in range(w):
            for y in range(h):
                point_map[x, y] = Point(f"{x}, {y}", w, 0, h, 0).set_position(x, y)
        
        return point_map


# Example usage:
if __name__ == "__main__":
    path_to_image = "pictures/maps/p11.png"
    # start_point = (0, 0)  # Replace with actual coordinates
    my_map = Map(path_to_image) #, start_point)
    # print(my_map.map.shape)
    plt.imshow(my_map.map)
    plt.show()
    # print(my_map.map.shape)
    
    # plt.imshow(my_map.map, cmap='gray')
    # plt.show()
    # You can use my_map.is_collide(x, y) to check collision
    # And my_map.paint(g) to draw the map
