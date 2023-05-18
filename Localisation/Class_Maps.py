import numpy as np
from spatialmath.base import *
import pandas as pd
import cv2



class Map:
    def __init__(self, floor_w = 4500, floor_h=7000, resolution = 10,
                    y_rotation=14, x_translation=0.5, z_translation = -1.0):
        self.imgh = int(floor_h/resolution) #map image heigh
        self.imgw = int(floor_w/resolution) #map image width
        self.resolution = resolution
        self.room_map = np.zeros((self.imgh,self.imgw,3), dtype=np.uint8)
        self.map = self.room_map.copy()

        # Convert angle from deg to radians
        theta = np.deg2rad(y_rotation)

        # Create 2D rotation matrix (rot_y)
        self.rot_y = np.array([[np.cos(theta), -np.sin(theta)],
                               [np.sin(theta), np.cos(theta)]])

        # create 2D rotation of 180 degrees about the x-axis
        self.rot_x = np.array([[1, 0],
                               [0, -1]])
      
        # create a translation about x axis
        self.trans_x = [[x_translation],
                                    [0]]
        
        # create a translation about z axis
        self.trans_z = [[0],
                        [z_translation]]        

    def feducial(self):
        r, c = self.bot_pos[0], self.bot_pos[1]
        fed = np.array([    [r, c],
                       [r+5, c-10],
                        [r-15,  c],
                        [r+5,c+10],
                            [r, c]],)
        
        angle = -self.tracker_angle_values_0_to_360

        # Convert the angle to radians
        angle = angle * np.pi / 180.0

        # Define the rotation matrix
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        rotation_matrix = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])

        # Translate the fiducial coordinates to origin
        translated_fed = fed - [r, c]

        # Rotate the fiducial by multiplying it with the rotation matrix
        rotated_fed = np.dot(translated_fed, rotation_matrix)

        # Translate the rotated fiducial back to its original position
        rotated_fed = rotated_fed + [r, c]

        # Convert the rotated fiducial to integer pixel coordinates
        rotated_fed = np.round(rotated_fed).astype(np.int32)

        return rotated_fed        
    
    def transforms(self,tracker_xz, tracker_theta):    #tracker_xz is 2x1 matrix

        p = self.rot_y @ tracker_xz
        p = self.rot_x @ p
        p = np.add(p, self.trans_x)
        self.tracker_coordinates = np.add(p, self.trans_z)   #tracker_coordinates is 2x1 matrix
        #print("refined_tracker_coordinates: ",tracker_coordinates, end="  ")

        self.img_c = int(self.tracker_coordinates[0][0]*1000/self.resolution)
        self.img_r = int(self.tracker_coordinates[1][0]*1000/self.resolution)
        self.bot_pos = (self.img_r, self.img_c)

        # Convert sensor values from -180 to 180 range to 0 to 360 range
        self.tracker_angle_values_0_to_360 = (tracker_theta + 360) % 360
        print("refined_tracker_theta: ", self.tracker_angle_values_0_to_360, end="")

        
        return self.bot_pos


    def get_map(self):   

        self.map = self.room_map.copy()       
        self.map = cv2.fillPoly(self.map, [self.feducial()], color = (0,69,255))

        return self.map
    



        
        