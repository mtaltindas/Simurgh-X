import os
import sys
import time
import smbus
import math

from imusensor.MPU9250 import MPU9250

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
imu.loadCalibDataFromFile("/home/simurgh/Codes/calib.json")
while True:
	imu.readSensor()
	imu.computeOrientation()
	newyaw=0
	newpitch=0
	newroll=0

	if imu.yaw<0 :
		newyaw=-1* imu.yaw
	else:
		newyaw=180+abs(imu.yaw-180)
	if imu.roll<0 :
		newroll=180+abs(imu.roll+180)
	else:
		newroll=imu.roll

	if imu.roll>180 :
		newroll=abs(imu.roll-180)
	else:
		newroll=360-abs(imu.roll-180)

	if imu.pitch<0 :
		newpitch=abs(imu.pitch)
	else:
		newpitch=360-abs(imu.pitch)
	
	#print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
	#print ("Gyro x: {0} ; Gyro y : {1} ; Gyro z : {2}".format(imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2]))
	#print ("Mag x: {0} ; Mag y : {1} ; Mag z : {2}".format(imu.MagVals[0], imu.MagVals[1], imu.MagVals[2]))
	print ("roll: {0} ; pitch : {1} ; yaw : {2}".format(int(newroll), int(newpitch), int(newyaw)))
	time.sleep(0.2)