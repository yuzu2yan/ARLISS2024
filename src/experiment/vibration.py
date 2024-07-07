import time
import board
import adafruit_bno055
import numpy as np
import datetime
import csv
import matplotlib.pyplot as plt

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)

def get_linear_acceleration(sensor):
    try:
        return sensor.linear_acceleration
    except Exception as e:
        return None

if __name__ == '__main__':
    date = datetime.datetime.now()
    start = date.strftime('%Y%m%d %H:%M:%S')
    filename = start + '_vibration-test.csv'
    
    accel_data = []
    time_data = []
    
    prev_accel = 0
    while True:
        try:
            linear_acceleration = get_linear_acceleration(sensor)
            if linear_acceleration is not None:
                accel = np.sqrt(linear_acceleration[0]**2 + linear_acceleration[1]**2 + linear_acceleration[2]**2) / 9.81
                prev_accel = accel
                if abs(accel - prev_accel) > 15:
                    continue
                print('accel : ', accel)
                now = datetime.datetime.now()
                passed_time = now - date
                accel_data.append(accel)
                time_data.append(passed_time.total_seconds())
                
                with open(filename, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([passed_time.total_seconds(), linear_acceleration[0], linear_acceleration[1], linear_acceleration[2], accel])
                
                time.sleep(0.01)
            else:
                continue
        except KeyboardInterrupt:
            break
        except Exception as e:
            time.sleep(0.1)


    plt.figure(figsize=(10, 6))
    plt.plot(time_data, accel_data, label='Acceleration (G)')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (G)')
    plt.title('Vibration test')
    plt.legend()
    plt.grid(True)
    plt.savefig(start + '_vibration-test.png')
    plt.show()
