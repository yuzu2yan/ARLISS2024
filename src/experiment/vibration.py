import time
import board
import adafruit_bno055
import numpy as np
import datetime
import csv
import matplotlib.pyplot as plt


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
    start = date.strftime('%Y%m%d %H:%M:%S')
    filename = start + '_vibration-test.csv'
    
    while True:
        try:
            accel = np.sqrt(sensor.linear_acceleration[0]**2 + sensor.linear_acceleration[1]**2 + sensor.linear_acceleration[2]**2)   
            print('accel : ', accel)
            now = datetime.datetime.now()
            passed_time = now - date
            with open(filename, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([passed_time, date.strftime('%H:%M:%S'), accel])
            f.close()
            
            time.sleep(0.01)
        except KeyboardInterrupt:
            time = np.linspace(0, passed_time.total_seconds(), len(accel))
            plt.plot(time, accel, label='Acceleration')
            plt.xlabel('time [s]')
            plt.ylabel('accel [m/s^2]')
            plt.title('Vibration test')
            plt.legend()
            plt.grid(True)
            
            plt.savefig(start + '_vibration-test.png')
            break    
        