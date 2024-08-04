"""""""""""""""""""""""""""""""""""
    ARLISS 2024
    ASTRUM OPEN CLASS MAIN PROGRAM
    
    Author : Yuzu
    Language : Python Ver.3.9.2
    Last Update : 08/05/2024
    Licence : MIT Licence
"""""""""""""""""""""""""""""""""""


import os
import logger
import time
import sys
import argparse
import datetime
import csv
import yaml
import gnss
import motor
import ground
import floating
import cone_detection
import send_location
from picamera2 import Picamera2
from ultralytics import YOLO


def main(phase=1):
    # Boot System
    print("--------------------SYSTEM START--------------------")
    try:
        now = datetime.datetime.now()
        directory_path = "./../data/" + now.strftime('%Y%m%d %H:%M:%S')
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        print('\033[32m' + "[INFO] Directory created." + '\033[0m')
        error_log = logger.ErrorLogger(directory_path)
        print('\033[32m' + "[INFO] Error logger created." + '\033[0m')
        drive = motor.Motor()
        drive.stop()
        print('\033[32m' + "[INFO] Motor activated." + '\033[0m')
        with open('settings.yaml') as yml:
            settings = yaml.safe_load(yml)
        des = [settings['destination']['longitude'], settings['destination']['latitude']]
        gnss.read_GPSData()
        print('\033[32m' + "[INFO] GNSS activated." + '\033[0m')
        floating.cal_altitude(0)
        print('\033[32m' + "[INFO] Barometric pressure sensor activated." + '\033[0m')
        ground.cal_heading_ang()
        print('\033[32m' + "[INFO] 9-Axis sensor activated." + '\033[0m')
        model = YOLO('../model/yolo.pt')
        print('\033[32m' + "[INFO] YOLO model loaded." + '\033[0m')
        picam2 = Picamera2()
        config = picam2.create_preview_configuration()
        picam2.configure(config)
        picam2.start()
        print('\033[32m' + "[INFO] Camera activated." + '\033[0m')
    except FileNotFoundError as e:
        print('\033[31m' + "[ERROR] File Not Found" + '\033[0m')
        with open('sys_error.csv', 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), 'File Not Found', str(e)])
            f.close()
        sys.exit()
    except Exception as e:
        print('\033[31m' + "Error : System start failed" + '\033[0m')
        with open('sys_error.csv', 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), 'Boot System Failed', str(e)])
            f.close()
        sys.exit()
    print("--------------------SYSTEM ALL GREEN--------------------")

    """
    phase 1 : Floating
          2 : Ground 
          3 : Image Processing
          4 : Reach the goal
    """


    """
    Floating Phase
    """
    if phase == 1:
        print("phase : ", phase)
        floating_log = logger.FloatingLogger(directory_path)
        """
        state 
            Rising
            Falling
            Landing
            Error
        """
        state = 'Rising'
        floating_log.state = 'Rising'
        init_altitude = 0
        data = floating.cal_altitude(init_altitude)
        init_altitude = data[2]
        altitude = init_altitude
        print("initial altitude : {}." .format(init_altitude))
        floating_log.floating_logger(data)
        print("Rising phase")
    while phase == 1:
        while state == 'Rising':
            data = floating.cal_altitude(init_altitude)
            altitude = data[2]
            floating_log.floating_logger(data)
            print("Rising")
            if altitude >= 25:
                state = 'Ascent Completed'
                floating_log.state = 'Ascent Completed'
            now = time.time()
            print("altitude : {}." .format(altitude))
            time.sleep(1.5)
        while state == 'Ascent Completed':
            data = floating.cal_altitude(init_altitude)
            altitude = data[2]
            floating_log.floating_logger(data)
            print("Falling")
            if altitude <= 4:
                state = 'Landing'
                floating_log.state = 'Landing'
                floating_log.end_of_floating_phase()
            print("altitude : {}." .format(altitude))
            phase = 2
            time.sleep(0.2)
        print("Landing")
        break

    if phase == 2 or phase == 3:
        drive.separate() # Separation mechanism activated
        drive.forward()
        time.sleep(3)
        drive.stop()
        reach_goal = False
        ground_log = logger.GroundLogger(directory_path)
        ground_log.state = 'Normal'
        img_proc_log = logger.ImgProcLogger(directory_path)
        

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
            send_location.send_gps(gps)
            data = ground.is_heading_goal(gps, des)
            distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
            print("distance : ", distance)
            ground_log.ground_logger(data, distance)
            # Goal judgment
            if distance <= settings['threshold']['close_to_goal_distance']: # Reach the goal within 8m
                print("Close to the goal")
                ground_log.end_of_ground_phase()
                phase = 3
                break
            count = 0
            while data[3] != True: # Not heading the goal
                if count > settings['threshold']['orientation'] or distance <= settings['threshold']['close_to_goal_distance']:
                    break
                if data[4] == 'Turn Right':
                    drive.turn_right()
                elif data[4] == 'Turn Left':
                    drive.turn_left()
                time.sleep(0.5)
                drive.forward()
                gps = gnss.read_GPSData()
                send_location.send_gps(gps)
                # The value used to check if the rover is heading towards the goal
                distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
                print("distance : ", distance)
                data = ground.is_heading_goal(gps, des)
                ground_log.ground_logger(data, distance)
                count += 1
            # End of Orientation Correction
            drive.forward()

                
        """
        Image Processing Phase
        """
        print("phase : ", phase)
        not_found = 0
        while phase == 3:
            drive.slowly_stop()
            time.sleep(3)
            gps = gnss.read_GPSData()
            send_location.send_gps(gps)
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
            if red_cone_percent >= settings['threshold']['red_cone_percent']:
                print("Reach the goal")
                phase = 4
                reach_goal = True
                img_proc_log.end_of_img_proc_phase()
                drive.forward()
                time.sleep(3)
                drive.stop()
                break
            elif cone_loc == "right":
                drive.turn_right()
                time.sleep(0.2)
            elif cone_loc == "left":
                drive.turn_left()
                time.sleep(0.2)
            elif cone_loc == "not found":
                not_found += 1
                if not_found >= settings['threshold']['cone_not_found']:
                    print('Error : Cone not found')
                    drive.stop()
                    phase = 2
                    break
                pre_ang = ground.cal_heading_ang()[0]
                while abs(pre_ang - ground.cal_heading_ang()[0]) < settings['threshold']['orientation_ang']:
                    drive.turn_right()
                    time.sleep(0.2)
            drive.forward()
            gps = gnss.read_GPSData()
            
    picam2.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='phase input')
    parser.add_argument('-p', '--phase', type=int, default=1)
    args = parser.parse_args()
    main(args.phase)