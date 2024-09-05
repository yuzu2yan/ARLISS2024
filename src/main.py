"""""""""""""""""""""""""""""""""""
    ARLISS 2024
    ASTRUM OPEN CLASS MAIN PROGRAM
    
    Author : Yuzu
    Language : Python Ver.3.9.2
    Last Update : 08/27/2024
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
import pigpio


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
        pi = pigpio.pi()
        handle = pi.i2c_open(1, 0x30)
        drive = motor.Motor(pi)
        drive.stop()
        print('\033[32m' + "[INFO] Motor activated." + '\033[0m')
        with open('settings.yaml') as yml:
            settings = yaml.safe_load(yml)
        des = [settings['destination']['longitude'], settings['destination']['latitude']]
        model = YOLO('../model/yolo.pt')
        print('\033[32m' + "[INFO] YOLO model loaded." + '\033[0m')
        camera_error = False
        picam2 = Picamera2()
        config = picam2.create_preview_configuration()
        picam2.configure(config)
        picam2.start()
        print('\033[32m' + "[INFO] Camera activated." + '\033[0m')
        print("--------------------SYSTEM ALL GREEN--------------------")
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
        print("initial altitude : {}." .format(init_altitude))
        floating_log.floating_logger(data)
        print("Rising phase")
    while phase == 1:
        while state == 'Rising':
            # gps = gnss.read_GPSData()
            # send_location.send_gps(gps)
            
            data = floating.cal_altitude(init_altitude)
            altitude = data[2]
            floating_log.floating_logger(data)
            print("Rising")
            if altitude >= settings['threshold']['rised_altitude']:
                state = 'Ascent Completed'
                floating_log.state = 'Ascent Completed'
            print("altitude : {}." .format(altitude))
            time.sleep(1.5)
        while state == 'Ascent Completed':
            gps = gnss.read_GPSData()
            try:
                send_location.send_gps(gps, pi, handle)
            except Exception as e:
                print("Error : ", e)
            data = floating.cal_altitude(init_altitude)
            altitude = data[2]
            floating_log.floating_logger(data)
            print("Falling")
            if altitude <= settings['threshold']['landed_altitude']:
                state = 'Landing'
                floating_log.state = 'Landing'
                floating_log.end_of_floating_phase()
            print("altitude : {}." .format(altitude))
            time.sleep(0.2)
        phase = 2
        print("Landing")
        time.sleep(settings['threshold']['wait_time'])
        break

    if phase == 2 or phase == 3:
        drive.separate() # Separation mechanism activated
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
            try:
                send_location.send_gps(gps, pi, handle)
            except Exception as e:
                print("Error : ", e)
            pre_gps = gps
            data = ground.is_heading_goal(gps, des)
            distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
            print("distance : ", distance)
            ground_log.ground_logger(data, distance)
            # Close to the goal
            if distance <= settings['threshold']['close_to_goal_distance']: # Reach the goal within 8m
                print("Close to the goal")
                ground_log.end_of_ground_phase()
                phase = 3
                break
            if camera_error and distance <= settings['threshold']['camera_error_distance']:
                print("Reaching the goal")
                ground_log.end_of_ground_phase()
                phase = 4
                break
            count = 0
            while data[3] != True: # Not heading the goal
                if count > settings['threshold']['orientation'] or distance <= settings['threshold']['close_to_goal_distance']:
                    break
                if data[4] == 'Turn Right':
                    drive.turn_right()
                elif data[4] == 'Turn Left':
                    drive.turn_left()
                time.sleep(1)
                drive.forward()
                gps = gnss.read_GPSData()
                try:
                    send_location.send_gps(gps, pi, handle)
                except Exception as e:
                    print("Error : ", e)
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
            if var != 0.0 and var < settings['threshold']['stuck_distance']:
                data = ground.is_heading_goal(gps, des)
                ground_log.state = 'Stuck'
                ground_log.ground_logger(data, distance)
                drive.stuck()
                ground_log.state = 'Normal'

                
        """
        Image Processing Phase
        """
        cone_loc = "not found"
        print("phase : ", phase)
        not_found = 0
        drive.slowly_stop()
        time.sleep(6)
        while phase == 3 and not camera_error:
            if cone_loc != "not found":
                drive.slowly_stop()
                time.sleep(3)
            gps = gnss.read_GPSData()
            try:
                send_location.send_gps(gps, pi, handle)
            except Exception as e:
                print("Error : ", e)
            distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
            print("distance : ", distance)
            if distance >= settings['threshold']['far_from_goal_distance']:
                print("Error : Far from the goal")
                phase = 2
                break
            try:
                percent, red_cone_percent, cone_loc, original_img_name, ditected_img_name = cone_detection.detect_cone(picam2, model, directory_path)
                img_proc_log.img_proc_logger(cone_loc, distance, percent, red_cone_percent,original_img_name, ditected_img_name)
                print("percent:", percent, "distance:", distance, "location:", cone_loc)
            except Exception as e:
                camera_error = True
                print("Error : Image processing failed")
                error_log.img_proc_error_logger(phase, distance)
                phase = 2
                drive.stop()
                break
            # Goal judgment
            if red_cone_percent >= settings['threshold']['red_cone_percent'] and percent >= settings['threshold']['cone_percent']:
                print("Reach the goal")
                phase = 4
                reach_goal = True
                img_proc_log.end_of_img_proc_phase()
                drive.forward()
                time.sleep(6)
                drive.stop()
                break
            elif cone_loc == "right":
                not_found = 0
                drive.turn_right()
                time.sleep(1)
            elif cone_loc == "left":
                not_found = 0
                drive.turn_left()
                time.sleep(1)
            elif cone_loc == "not found":
                not_found += 1
                if not_found >= settings['threshold']['cone_not_found']:
                    print('Cone not found')
                    img_proc_log.not_found_logger(distance)
                    drive.stop()
                    phase = 2
                    break
                pre_ang = ground.cal_heading_ang()[0]
                while (abs(pre_ang - ground.cal_heading_ang()[0]) < settings['threshold']['orientation_ang']):
                    drive.turn_here()
                    time.sleep(0.1)
                drive.stop()
            else: # front
                not_found = 0
                # continue
            # drive.forward()
            # gps = gnss.read_GPSData()
            
    picam2.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='phase input')
    parser.add_argument('-p', '--phase', type=int, default=1)
    args = parser.parse_args()
    main(args.phase)