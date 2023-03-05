'''
altitude,temperature=getAltitude() 
Ax,Ay,Az=imu.getAccel()
Gx,Gy,Gz=imu.getGyro()
bearing=getMagnetometer()
'''

from Ivme_Olcer import mpu6050Sensor
from Basinc_Olcer import bmp180Sensor

import time
#from . import hmc5883l


imu=mpu6050Sensor(port=0)
imu.MPU_Init()
while True:
	roll,pitch=imu.getAngles()
	yaw=imu.get_yaw()
	print(int(roll),int(pitch),int(yaw))
	time.sleep(0.5)
'''
hmc=hmc5883l()

'''
'''
bmp=bmp180Sensor(port=0)
bmp.calibrate()
while True:
	altitude,temperature=bmp.getAltitude(False) 
	print(altitude)
	time.sleep(0.1)
'''



time.sleep(0.3)



