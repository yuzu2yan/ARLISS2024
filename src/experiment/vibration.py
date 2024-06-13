import time
import board
import adafruit_bno055
import numpy as np


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
    # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    # # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    # # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    # # print("Euler angle: {}".format(sensor.euler))
    # # print("Quaternion: {}".format(sensor.quaternion))
    # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    # print("Gravity (m/s^2): {}".format(sensor.gravity))
    # print()
    
    accecl = np.sqrt(sensor.linear_acceleration[0]**2 + sensor.linear_acceleration[1]**2 + sensor.linear_acceleration[2]**2)
    print("Linear acceleration (m/s^2): {}".format(accecl))

    time.sleep(1)