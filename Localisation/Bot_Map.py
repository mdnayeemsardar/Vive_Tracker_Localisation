import time

while True:
    try:
        from Class_LiDAR import LidarVisualizer
        from Class_Tracker import ViveTracker
        import cv2

        lidar = LidarVisualizer()
        trk = ViveTracker()

        # create an empty numpy array to hold the image
        image = None

        for map_data in lidar.start():

            trk_map = trk.get_tracker_data()

            # convert the dimensions and channels of map_data same as trk_map....viz,. (700,450,3)
            map_data = cv2.cvtColor(map_data, cv2.COLOR_GRAY2BGR)

            # bitwise_or operation on both the images
            or_img = cv2.bitwise_or(map_data, trk_map)

            # update the image with the latest frame
            image = or_img

            # show the image
            cv2.imshow('Tracker Map', image)

            # save the image as a .png file
            cv2.imwrite('updated_image.png', image)

            if cv2.waitKey(1) == ord('q'):
                break

        #lidar.stop()
        cv2.destroyAllWindows()

    except Exception as e:
        print("An error occurred:", e)
        print("Retrying in 5 seconds...")
        #lidar.stop()
        cv2.destroyAllWindows()
        time.sleep(2)  # wait for 2 seconds before attempting to run the program again
