import gnss
import pigpio
import time

def send_gps(gps, pi):
    handle = pi.i2c_open(1, 0x30)
    try:
        pi.i2c_write_device(handle, str(gps[0]))
        pi.i2c_write_device(handle, str(gps[1]))
        time.sleep(1)
    except Exception as e:
        # pi.i2c_close(handle)
        # pi.stop()        
        print("Error : ", e)

    
if __name__ == '__main__':
    pi = pigpio.pi()
    while True:
        gps = gnss.read_GPSData()
        if gps == [0,0]:
            print("Waiting for GPS reception")
            time.sleep(5)
            continue
        print("GPS data : ", gps)    
        send_gps(gps, pi)