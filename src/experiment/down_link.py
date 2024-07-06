import sys
sys.path.append('./../')
import gnss
import pigpio
import time
import datetime
import csv
import struct

def main():
    pi = pigpio.pi()
    handle = pi.i2c_open(1, 0x04)
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d %H:%M:%S') + ".csv"
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['longitude', 'latitude'])
    try:
        while True:
            gps = gnss.read_GPSData()
            if gps == [0,0]:
                print("Waiting for GPS reception")
                # time.sleep(5)
            with open(filename, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([gps[0], gps[1]])
            gps = struct.pack('f', gps[0], gps[1])
            pi.i2c_write_device(handle, gps)
            time.sleep(1)
    except KeyboardInterrupt:
        pi.i2c_close(handle)
        pi.stop()        
    
    
if __name__ == '__main__':
    main()