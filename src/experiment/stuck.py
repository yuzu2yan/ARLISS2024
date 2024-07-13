import sys
sys.path.append('./../')
import motor
import gnss
import ground
import time

def stuck():
    drive = motor.Motor()
    while True:
        drive.forward()
        pre_gps = gnss.read_GPSData()
        time.sleep(5)
        gps = gnss.read_GPSData()
        distance = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])
        if distance < 0.1:
            drive.stuck()
            drive.stop()
            return



if __name__ == '__main__':
    stuck()