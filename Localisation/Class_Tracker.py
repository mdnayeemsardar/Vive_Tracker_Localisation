import triad_openvr
import time
import sys
from Class_Maps import *
import cv2

class ViveTracker:
    def __init__(self, interval=1/250):
        self.v = triad_openvr.triad_openvr()
        self.v.print_discovered_objects()
        self.maps = Map()
        self.interval = interval

    def get_tracker_data(self):
        txt = ""
        for each in self.v.devices["tracker_1"].get_pose_euler():
            txt += "%.4f" % each
            txt += " "
        l = list(map(float, txt.split()))
        tracker_xz = [[l[0]],
                     [l[2]]]
        tracker_theta = l[4] 

        self.maps.transforms(tracker_xz, tracker_theta)

        map_img = self.maps.get_map()
        return map_img#, tracker_xz
        #remove , tracker_xz from the return statement when u run Bot_map.py file


    
    def run(self):
    #use when wanna get only the tracker map
        while(True):
            start = time.time()

            map_img = self.get_tracker_data()

            cv2.imshow("Live",map_img)
            cv2.waitKey(1)
            sleep_time = self.interval-(time.time()-start)
            if sleep_time>0:
                time.sleep(sleep_time)
