import numpy as np
from rplidar import RPLidar
import cv2
from Class_Tracker import ViveTracker


class LidarVisualizer:

    def __init__(self, port='COM3', resolution=10, width=450, height=700):
        self.port = port
        self.resolution = resolution
        self.width = width
        self.height = height
        self.image = np.zeros((self.height, self.width), dtype=np.uint8)
        self.lidar = RPLidar(self.port)

    def start(self):
        self.lidar.start_motor()
        for scan in self.lidar.iter_scans():
            self.image.fill(0)
            #map_img = ViveTracker.get_tracker_data()

        
            for (_, angle, distance) in scan:
                x = int(distance * np.sin(np.radians(angle)) / self.resolution + self.width // 2)
                y = int(distance * np.cos(np.radians(angle)) / self.resolution + self.height // 2)
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.image[y, x] = 255
                    #yield x,y
                    #print(y,x) 

            cv2.drawMarker(self.image, (self.width // 2, self.height // 2), (255, 0, 0),
                           cv2.MARKER_TRIANGLE_UP, markerSize=10, thickness=2)

            map_data = self.image.copy()

            yield map_data

    def stop(self):
        self.lidar.stop_motor()

    '''

if __name__ == '__main__':

    lidar = LidarVisualizer()
    trk = ViveTracker()
    for map_data in lidar.start():

        trk_map = trk.get_tracker_data()
        
        #convert the dimensions and channels of map_data same as trk_map....viz,. (700,450,3)
        map_data = cv2.cvtColor(map_data, cv2.COLOR_GRAY2BGR)

        #bitwise_or operation on both the images
        or_img = cv2.bitwise_or(map_data,trk_map)

        cv2.imshow('Tracker Map', or_img)
        if cv2.waitKey(1) == ord('q'):
            break
    lidar.stop()
    cv2.destroyAllWindows()


'''