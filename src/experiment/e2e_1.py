import os
import sys
sys.path.append('./../')
import logger
import time
import datetime
import motor
import floating


def main():
    """
    Floating Phase
    """
    drive = motor.Motor()
    phase = 1
    if phase == 1:
        print("phase : ", phase)
        now = datetime.datetime.now()
        directory_path = "../../data/" + now.strftime('%Y%m%d %H:%M:%S')
        os.makedirs(directory_path)
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
        start = time.time()
        # The flag that identifies abnormalities in the barometric pressure sensor
        error_baro = 0
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
            # Incorrect sensor value
            if altitude < -5:
                error_baro += 1
                if error_baro >= 15:
                    state = 'Error'
                    floating_log.state = 'Error'
                    print("Error : Altitude value decreases during ascent")
                time.sleep(1.5)
                continue
            if altitude >= 5:
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
            if altitude <= 2:
                state = 'Landing'
                floating_log.state = 'Landing'
                floating_log.end_of_floating_phase()
            now = time.time()
            print("altitude : {}." .format(altitude))
            time.sleep(0.2)
            
        print("Landing")
        phase = 2
        break


    drive.separate() # Separation mechanism activated
    drive.forward()
    time.sleep(3)
    drive.stop()

if __name__ == '__main__':
    main()