import pigpio
import time

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html
FRONT = [27, 9] # Left, Right
REAR = [4, 10] # Left, Right
SEPA_FIN = 20
SEPA_RIN = 21
PINS = FRONT + REAR + [SEPA_FIN, SEPA_RIN]
class Motor(object):
    def __init__(self):
        Motor.pi = pigpio.pi()
        self.max_dutyrate = 1.0
        for pin in PINS:
            Motor.pi.set_mode(pin, pigpio.OUTPUT)
            Motor.pi.set_PWM_frequency(pin, 10000)
            Motor.pi.set_PWM_range(pin, 100)
            
    
    def forward(self):
        [Motor.pi.set_PWM_dutycycle(pin, 100) for pin in FRONT]
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("forward")
        
    def back(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in FRONT]
        [Motor.pi.set_PWM_dutycycle(pin, 100) for pin in REAR]
        print("back")
    
    def stop(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in PINS]
        print("stop")
        
    def turn_right(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], 90 * 0.7 * self.max_dutyrate) # Left
        Motor.pi.set_PWM_dutycycle(FRONT[1], 100 * self.max_dutyrate) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn right")
    
    def turn_left(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], 90* self.max_dutyrate) # Left
        Motor.pi.set_PWM_dutycycle(FRONT[1], self.max_dutyrate * 0.7) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn left")
        
    def separate(self):
        # Motor.pi.set_PWM_dutycycle(SEPA_FIN, 50) 
        # Motor.pi.set_PWM_dutycycle(SEPA_RIN, 0)
        # time.sleep(3)
        # self.stop()
        # print("parachute separated")
        Motor.pi.write(SEPA_FIN, 1)
        Motor.pi.write(SEPA_RIN, 0)
        
                
    def attach_para(self):
        # Motor.pi.set_PWM_dutycycle(SEPA_FIN, 0) 
        # Motor.pi.set_PWM_dutycycle(SEPA_RIN, 50) 
        # print("parachute attached")
        Motor.pi.write(SEPA_FIN, 0)
        Motor.pi.write(SEPA_RIN, 1)

if __name__ == '__main__':
    drive = Motor()
    movement = {'w': drive.forward, 'a': drive.turn_left, 's': drive.back, 'd':drive.turn_right, 'q': drive.stop, 'sep': drive.separate, 'para': drive.attach_para}
    while True:
        c = input('Enter char : ')
        if c in movement.keys():
            movement[c]()
        elif c == 'z':
            break
        else:
            print('Invalid input')
