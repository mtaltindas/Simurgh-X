import smbus            #import SMBus module of I2C
from time import sleep          #import
import math 
import time


from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685


i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50
servo0 = servo.Servo(pca.channels[0])
servo1= servo.Servo(pca.channels[1])
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians) 
def calcIMUError():
	AccErrorX=0
	AccErrorY=0
	c=0
	while(c<200):
		acc_x = read_raw_data(ACCEL_XOUT_H)
		acc_y = read_raw_data(ACCEL_YOUT_H)
		acc_z = read_raw_data(ACCEL_ZOUT_H)
		 
		 
		#Full scale range +/- 250 degree/C as per sensitivity scale factor
		Ax = acc_x/16384.0
		Ay = acc_y/16384.0
		Az = acc_z/16384.0
		AccErrorX = AccErrorX + ((math.atan((Ay) / math.sqrt(math.pow((Ax), 2) + math.pow((Az), 2))) * 180 / math.pi))
		AccErrorY = AccErrorY + ((math.atan(-1 * (Ax) / math.sqrt(math.pow((Ay), 2) + math.pow((Az), 2))) * 180 / math.pi))
		c+=1
	AccErrorX=AccErrorX/200
	AccErrorY=AccErrorY/200

	GyroErrorX=0
	GyroErrorY=0
	GyroErrorZ=0
	c=0
	while(c<200):
		gyro_x = read_raw_data(GYRO_XOUT_H)
		gyro_y = read_raw_data(GYRO_YOUT_H)
		gyro_z = read_raw_data(GYRO_ZOUT_H)
		 
		Gx = gyro_x/131.0
		Gy = gyro_y/131.0
		Gz = gyro_z/131.0
		GyroErrorX = GyroErrorX + (Gx)
		GyroErrorY = GyroErrorY + (Gy)
		GyroErrorZ = GyroErrorZ + (Gz)
		c+=1
	GyroErrorX=GyroErrorX/200
	GyroErrorY=GyroErrorY/200
	GyroErrorZ=GyroErrorZ/200
	return AccErrorX,AccErrorY,GyroErrorX,GyroErrorY,GyroErrorZ
 
def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
     
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
     
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
     
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
     
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)
 
def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
     
        #concatenate higher and lower value
        value = ((high << 8) | low)
         
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
 
 
bus = smbus.SMBus(0)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address
 
MPU_Init()

#AccErrorX,AccErrorY,GyroErrorX,GyroErrorY,GyroErrorZ=calcIMUError()

print (" Reading Data of Gyroscope and Accelerometer")
gAngleX=0
gAngleY=0 
yaw=0
curTime=time.time() 
time.sleep(0.6)
gyro_z = read_raw_data(GYRO_ZOUT_H)
Gz = (gyro_z/131.0)#+GyroErrorZ
ZRotation=0


while True:
	ZRotation+=(Gz-0.03) 
    #Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
     
    #Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
     
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
     
	Gx = (gyro_x/131.0)#+GyroErrorX
	Gy = (gyro_y/131.0)#-GyroErrorY
	Gz = (gyro_z/131.0)#+GyroErrorZ
	accAngleX=(math.atan(Ay/math.sqrt(math.pow(Ax,2)+math.pow(Az,2)))*180/math.pi)#-AccErrorX
	accAngleY=(math.atan(-1*Ax/math.sqrt(math.pow(Ay,2)+math.pow(Az,2)))*180/math.pi)#+AccErrorY

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




