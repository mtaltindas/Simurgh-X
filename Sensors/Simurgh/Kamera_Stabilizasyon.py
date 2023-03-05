import smbus            #import SMBus module of I2C
from time import sleep          #import
import math 
import time


from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

from Ivme_Olcer import mpu6050Sensor

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50
servo0 = servo.Servo(pca.channels[0])
servo1= servo.Servo(pca.channels[1])

imu=mpu6050Sensor(port=0) 
MPU_Init()


print (" Reading Data of Gyroscope and Accelerometer")
gAngleX=0
gAngleY=0 
yaw=0
curTime=time.time() 
time.sleep(0.6)
gyro_z = read_raw_data(GYRO_ZOUT_H)
Gz = (gyro_z/131.0)+GyroErrorZ
ZRotation=0

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
servo_lock=165
servo_release=350
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

while True:
	ZRotation+=(Gz-0.03) 
    #Read Accelerometer raw value
    acc_x,acc_y,acc_z=imu.getAccel() 
    #Read Gyroscope raw value
    gyro_x,gyro_y,gyro_z=imu.getGyro() 
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
     
	Gx = (gyro_x/131.0)+GyroErrorX
	Gy = (gyro_y/131.0)-GyroErrorY
	Gz = (gyro_z/131.0)+GyroErrorZ
	accAngleX=(math.atan(Ay/math.sqrt(math.pow(Ax,2)+math.pow(Az,2)))*180/math.pi)-AccErrorX
	accAngleY=(math.atan(-1*Ax/math.sqrt(math.pow(Ay,2)+math.pow(Az,2)))*180/math.pi)+AccErrorY

	prevTime=curTime
	curTime=time.time()
	elapsedTime=curTime-prevTime
	gAngleX= gAngleX+Gx*elapsedTime
	gAngleY= gAngleY+Gz*elapsedTime
	yaw=yaw+Gz*elapsedTime

	roll=0.96*gAngleX+0.04*accAngleX
	pitch=0.96*gAngleY+0.04*accAngleY
	XRotation=get_x_rotation(Ax, Ay, Az)
	YRotation=get_y_rotation(Ax, Ay, Az)
	ZRotation
	#print("Roll",roll,"Pitch",pitch,"Yaw",yaw)
	#print ("X Rotation: " , get_x_rotation(Ax, Ay, Az))
	#print ("Y Rotation: " , get_y_rotation(Ax, Ay, Az))	
	print("Z Rotation: " ,ZRotation)
	
	pwmSignalY=int((YRotation+40)*(180/80))
	
	pwmSignalZ=int((ZRotation+40)*(180/80))
	if (ZRotation>40):
		pwmSignalZ=180

	time.sleep(0.05)

	servo0.angle = pwmSignalY
	servo1.angle = pwmSignalZ
	sleep(0.03)



print('Moving servo on channel 0, press Ctrl-C to quit...')

# Move servo on channel O between extremes.




