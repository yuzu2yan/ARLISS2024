import pigpio
import time

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html
FRONT = [13, 27]  # Left, Right
REAR = [19, 17]   # Left, Right
SEPA_FIN = 10
SEPA_RIN = 9
PINS = FRONT + REAR + [SEPA_FIN, SEPA_RIN]

class Motor(object):
    def __init__(self, pi):
        self.pi = pi
        for pin in PINS:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.set_PWM_frequency(pin, 10000)
            self.pi.set_PWM_range(pin, 100)

    def forward(self):
        [self.pi.set_PWM_dutycycle(pin, 100) for pin in FRONT]
        [self.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("forward")

    def back(self):
        [self.pi.set_PWM_dutycycle(pin, 0) for pin in FRONT]
        [self.pi.set_PWM_dutycycle(pin, 100) for pin in REAR]
        print("back")

    def stop(self):
        [self.pi.set_PWM_dutycycle(pin, 0) for pin in PINS]
        print("stop")

    def slowly_stop(self):
        for i in range(100, 0, -1):
            [self.pi.set_PWM_dutycycle(pin, i) for pin in FRONT]
            [self.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
            time.sleep(0.06)
        print("slowly stop")

    def turn_right(self):
        self.pi.set_PWM_dutycycle(FRONT[1], 100)  # Left
        self.pi.set_PWM_dutycycle(FRONT[0], 10)   # Right
        [self.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn right")

    def turn_left(self):
        self.pi.set_PWM_dutycycle(FRONT[1], 10)  # Left
        self.pi.set_PWM_dutycycle(FRONT[0], 100) # Right
        [self.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn left")

    def turn_here(self):
        self.pi.set_PWM_dutycycle(FRONT[1], 20)  # Left
        self.pi.set_PWM_dutycycle(FRONT[0], 0)   # Right
        self.pi.set_PWM_dutycycle(REAR[1], 0)    # Left
        self.pi.set_PWM_dutycycle(REAR[0], 20)   # Right

    def stuck(self):
        print("stuck")
        self.stop()
        self.back()
        time.sleep(5)
        self.stop()
        print("stuck process end")

    def separate(self):
        self.pi.set_PWM_dutycycle(SEPA_FIN, 50) 
        self.pi.set_PWM_dutycycle(SEPA_RIN, 0)
        time.sleep(3)
        self.stop()
        print("parachute separated")

    def attach_para(self):
        self.pi.set_PWM_dutycycle(SEPA_FIN, 0) 
        self.pi.set_PWM_dutycycle(SEPA_RIN, 50) 
        print("parachute attached")

if __name__ == '__main__':
    pi = pigpio.pi()  # pigpioインスタンスの作成
    drive = Motor(pi)  # Motorクラスにインスタンスを渡す
    movement = {
        'w': drive.forward,
        'a': drive.turn_left,
        's': drive.back,
        'd': drive.turn_right,
        'q': drive.stop,
        'sep': drive.separate,
        'para': drive.attach_para,
        'stuck': drive.stuck,
        'sl': drive.slowly_stop,
        'th': drive.turn_here
    }
    while True:
        c = input('Enter char : ')
        if c in movement.keys():
            movement[c]()
        elif c == 'z':
            break
        else:
            print('Invalid input')
