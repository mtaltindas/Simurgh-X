import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=0,reference_clock_speed=500)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
servo_lock=165
servo_release=350
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)

print('Moving servo on channel 0, press Ctrl-C to quit...')
'''
# Move servo on channel O between extremes.
time.sleep(1)
pwm.set_pwm(0, 0, servo_lock)
time.sleep(5)
pwm.set_pwm(0, 0, servo_release)
time.sleep(2)
#pwm.set_pwm(0, 0, servo_max)
#time.sleep(2)

'''
for i in range(150,400,5):
	time.sleep(0.1)
	pwm.set_pwm(0, 0, i)
	pwm.set_pwm(1, 0, i)
time.sleep(1)

for i in range(400,150,-5):
	time.sleep(0.1)
	pwm.set_pwm(0, 0, i)
	pwm.set_pwm(1, 0, i)


