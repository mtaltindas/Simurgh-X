
from time import sleep          #import
import math 
import time
import os
import sys
import smbus
from imusensor.MPU9250 import MPU9250

from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685


address = 0x68
bus = smbus.SMBus(0)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
imu.loadCalibDataFromFile("/home/simurgh/Codes/calib.json")




i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50
servo0 = servo.Servo(pca.channels[0])
servo1= servo.Servo(pca.channels[1])

imu.readSensor()
imu.computeOrientation()
print (" pitch : {0} ; yaw : {1}".format( int(imu.pitch), int(imu.yaw)))
prev_pitch_angle=imu.pitch
prev_yaw_angle=imu.yaw
pwmSignalY=90
pwmSignalZ=90
servo0.angle = 90
servo1.angle = 90
while True:
	imu.readSensor()
	imu.computeOrientation()
	print ("pitch : {0} ; yaw : {1}".format(int(imu.pitch), int(imu.yaw)))

	if (imu.pitch-prev_pitch_angle)>5:
		if(pwmSignalY-(imu.pitch-prev_pitch_angle)>180 or pwmSignalY-(imu.pitch-prev_pitch_angle)<0):
			pass
		else:
			pwmSignalY=pwmSignalY-(imu.pitch-prev_pitch_angle)
	if (imu.yaw-prev_yaw_angle)>5:
		if(pwmSignalZ-(imu.yaw-prev_yaw_angle)>180 or pwmSignalZ-(imu.yaw-prev_yaw_angle)<0):
			pass
		else:
			pwmSignalZ=pwmSignalZ-(imu.yaw-prev_yaw_angle)
	prev_yaw_angle=imu.yaw
	prev_pitch_angle=imu.pitch

	time.sleep(0.05)

	servo0.angle = pwmSignalY
	servo1.angle = pwmSignalZ
	sleep(0.03)



print('Moving servo on channel 0, press Ctrl-C to quit...')

# Move servo on channel O between extremes.




