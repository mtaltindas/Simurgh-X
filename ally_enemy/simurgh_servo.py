import time

# Import the PCA9685 module.
import Adafruit_PCA9685


class SimurghServo:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=0)

        self.servo_min = 150  # Min pulse length out of 4096
        self.servo_max = 600  # Max pulse length out of 4096
        self.servo_lock=165
        self.servo_release=350
        self.pwm.set_pwm_freq(50)
        
    def releaseSupplyKit(self):
        print('Moving servo on channel 0, press Ctrl-C to quit...')
        time.sleep(1)
        self.pwm.set_pwm(0, 0, self.servo_release)
    def lockSupplyKit(self):
        time.sleep(1)
        self.pwm.set_pwm(0, 0, self.servo_lock)

#pwm.set_pwm(0, 0, servo_max)
#time.sleep(2)
