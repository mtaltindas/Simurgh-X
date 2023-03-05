
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




while True:
	imu.readSensor()
	imu.computeOrientation()
	print ("roll: {0} ; pitch : {1} ; yaw : {2}".format(int(imu.roll), int(imu.pitch), int(imu.yaw)))
	#print("Roll",roll,"Pitch",pitch,"Yaw",yaw)
	#print ("X Rotation: " , get_x_rotation(Ax, Ay, Az))
	#print ("Y Rotation: " , get_y_rotation(Ax, Ay, Az))	
	print("Z Rotation: " ,ZRotation)
	
	pwmSignalY=int((imu.pitch+40)*(180/80))
	pwmSignalZ=int((imu.yaw+40)*(180/80))

	time.sleep(0.05)

	servo0.angle = pwmSignalY
	servo1.angle = pwmSignalZ
	sleep(0.03)



print('Moving servo on channel 0, press Ctrl-C to quit...')

# Move servo on channel O between extremes.




