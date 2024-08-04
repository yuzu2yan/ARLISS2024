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
    try:
        while True:
            gps = gnss.read_GPSData()
            if gps == [0,0]:
                print("Waiting for GPS reception")
                time.sleep(5)
                continue
            print('longitude : ', gps[0], 'latitude : ', gps[1])
            pi.i2c_write_device(handle, str(gps[0]))
            pi.i2c_write_device(handle, str(gps[1]))
            time.sleep(1)
    except KeyboardInterrupt:
        pi.i2c_close(handle)
        pi.stop()        
    
    
if __name__ == '__main__':
    main()