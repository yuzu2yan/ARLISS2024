import os
import time
import sys
sys.path.append('./../')
import logger
import datetime
import csv
import yaml
import cv2
import gnss
import motor
import ground
import cone_detection
from picamera2 import Picamera2
from ultralytics import YOLO


def main():
    des = [139.65338833333334, 35.950298333333336]
    """
    phase 1 : Floating
          2 : Ground 
          3 : Image Processing
          4 : Reach the goal
    """
    drive = motor.Motor()
    drive.stop()
    reach_goal = False
    phase = 2
    now = datetime.datetime.now()
    directory_path = "../../data/" + now.strftime('%Y%m%d %H:%M:%S')
    os.makedirs(directory_path)
    ground_log = logger.GroundLogger(directory_path)
    ground_log.state = 'Normal'

    img_proc_log = logger.ImgProcLogger(directory_path)
    img_proc_log.state = 'Normal'
    model = YOLO('./best.pt')
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()

    while not reach_goal:
        """
        Ground Phase
        """
        print("phase : ", phase)
        while gnss.read_GPSData() == [0,0]:
                print("Waiting for GPS reception")
                time.sleep(5)
        while phase == 2:
            gps = gnss.read_GPSData()
            pre_gps = gps
            data = ground.is_heading_goal(gps, des)
            distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
            print("distance : ", distance)
            ground_log.ground_logger(data, distance)
            # Goal judgment
            if distance <= 8: # Reach the goal within 8m
                print("Close to the goal")
                ground_log.end_of_ground_phase()
                phase = 3
                break
            count = 0
            while data[3] != True: # Not heading the goal
                if count > 7 or distance <= 8:
                    break
                if data[4] == 'Turn Right':
                    drive.turn_right()
                elif data[4] == 'Turn Left':
                    drive.turn_left()
                time.sleep(0.5)
                drive.forward()
                gps = gnss.read_GPSData()
                # The value used to check if the rover is heading towards the goal
                distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
                print("distance : ", distance)
                data = ground.is_heading_goal(gps, des)
                ground_log.ground_logger(data, distance)
                count += 1
            # End of Orientation Correction
            drive.forward()
            time.sleep(3)
            gps = gnss.read_GPSData()
            var = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])   
            if var < 1:
                drive.stuck()

                
        """
        Image Processing Phase
        """
        print("phase : ", phase)
        not_found = 0
        while phase == 3:
            drive.slowly_stop()
            time.sleep(3)
            gps = gnss.read_GPSData()
            pre_gps = gps
            distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
            print("distance : ", distance)
            try:
                percent, red_cone_percent, cone_loc, original_img_name, ditected_img_name = cone_detection.detect_cone(picam2, model, directory_path)
                img_proc_log.img_proc_logger(cone_loc, distance, percent, red_cone_percent,original_img_name, ditected_img_name)
                print("percent:", percent, "distance:", distance, "location:", cone_loc)
            except Exception as e:
                    print("Error : Image processing failed")
                    phase = 4
                    reach_goal = True
                    with open('sys_error.csv', 'a') as f:
                        now = datetime.datetime.now()
                        writer = csv.writer(f)
                        writer.writerow([now.strftime('%H:%M:%S'), 'Image processing failed', str(e)])
                        f.close()
                    drive.stop()
                    break
            # Goal judgment
            if red_cone_percent >= 30:
                print("Reach the goal")
                phase = 4
                reach_goal = True
                img_proc_log.end_of_img_proc_phase()
                drive.forward()
                time.sleep(3)
                drive.stop()
                break
            if cone_loc == "right":
                drive.turn_right()
                time.sleep(0.2)
            elif cone_loc == "left":
                drive.turn_left()
                time.sleep(0.2)
            elif cone_loc == "not found":
                not_found += 1
                if not_found >= 10:
                    print('Error : Cone not found')
                    drive.stop()
                    phase = 2
                    break
                pre_ang = ground.cal_heading_ang()[0]
                while abs(pre_ang - ground.cal_heading_ang()[0]) > 45:
                    drive.turn_right()
                    time.sleep(0.2)
            drive.forward()
            gps = gnss.read_GPSData()
            var = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])
            if var < 1:
                drive.stuck()
            
    picam2.stop()


if __name__ == '__main__':
    main()