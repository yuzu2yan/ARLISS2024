import pigpio
import struct
import time

I2C_ADDRESS = 0x08 

pi = pigpio.pi()

handle = pi.i2c_open(1, I2C_ADDRESS)

def float_to_bytes(value):
    return bytearray(struct.pack("d", value))

def send_data(latitude, longitude):
    try:
        lat_bytes = float_to_bytes(latitude)
        lon_bytes = float_to_bytes(longitude)
        
        pi.i2c_write_i2c_block_data(handle, 0x00, lat_bytes)
        time.sleep(0.1)  # wait for 0.1 sec
        pi.i2c_write_i2c_block_data(handle, 0x01, lon_bytes)
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    latitude = 35.68954321
    longitude = 139.69174321  
    
    try:
        while True:
            send_data(latitude, longitude)
            time.sleep(1)  # wait for 1 sec
    except KeyboardInterrupt:
        pass
    finally:
        pi.i2c_close(handle)
        pi.stop()
