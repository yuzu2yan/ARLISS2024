import time
import board
import adafruit_bno055
import numpy as np
import datetime
import csv


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_bno055.BNO055_I2C(i2c)

# while True:
    # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    # # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    # # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    # # print("Euler angle: {}".format(sensor.euler))
    # # print("Quaternion: {}".format(sensor.quaternion))
    # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    # print("Gravity (m/s^2): {}".format(sensor.gravity))
    # print()
    
    # time.sleep(1)

    
if __name__ == '__main__':
    date = datetime.datetime.now()
    filename = date.strftime('%Y%m%d %H:%M:%S') + '_vibration-test.csv'
    
    while True:
        accecl = np.sqrt(sensor.linear_acceleration[0]**2 + sensor.linear_acceleration[1]**2 + sensor.linear_acceleration[2]**2)   
        print('accel : ', accecl)
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([date.strftime('%H:%M:%S'), accecl])
        f.close()
        
        time.sleep(0.01)