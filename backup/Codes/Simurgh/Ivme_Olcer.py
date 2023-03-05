import smbus            #import SMBus module of I2C
from time import sleep,time          #import
import math
class mpu6050Sensor: 

    def __init__(self,port,i2cAddress=0x68):
        #some MPU6050 Registers and their Address
        self.PWR_MGMT_1   = 0x6B
        self.SMPLRT_DIV   = 0x19
        self.CONFIG       = 0x1A
        self.GYRO_CONFIG  = 0x1B
        self.INT_ENABLE   = 0x38
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.GYRO_XOUT_H  = 0x43
        self.GYRO_YOUT_H  = 0x45
        self.GYRO_ZOUT_H  = 0x47
    
        self.bus = smbus.SMBus(port)    # or bus = smbus.SMBus(0) for older version boards
        self.Device_Address =i2cAddress    # MPU6050 device address
    
        self.yaw=0
        self.prevTime=time()

    def MPU_Init(self):
        #write to sample rate register
        self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 7)
        
        #Write to power management register
        self.bus.write_byte_data(self.Device_Address, self.PWR_MGMT_1, 1)
        
        #Write to Configuration register
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)
        
        #Write to Gyro configuration register
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)
        
        #Write to interrupt enable register
        self.bus.write_byte_data(self.Device_Address, self.INT_ENABLE, 1)
    
    def read_raw_data(self,addr):
        #Accelero and Gyro value are 16-bit
            high = self.bus.read_byte_data(self.Device_Address, addr)
            low = self.bus.read_byte_data(self.Device_Address, addr+1)
        
            #concatenate higher and lower value
            value = ((high << 8) | low)
            
            #to get signed value from mpu6050
            if(value > 32768):
                    value = value - 65536
            return value

    def getAccel(self): 
        acc_x = self.read_raw_data(self.ACCEL_XOUT_H)
        acc_y = self.read_raw_data(self.ACCEL_YOUT_H)
        acc_z = self.read_raw_data(self.ACCEL_ZOUT_H)     
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        return Ax,Ay,Az

    def getGyro(self):
        #Read Gyroscope raw value
        gyro_x = self.read_raw_data(self.GYRO_XOUT_H)
        gyro_y = self.read_raw_data(self.GYRO_YOUT_H)
        gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)

        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0 
        return Gx,Gy,Gz
    def dist(self,a,b):
        return math.sqrt((a*a)+(b*b))
 
    def get_y_rotation(self,x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)
    
    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians) 
    def get_yaw(self):
        prevRes=self.yaw

        gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)
        Gz = gyro_z/131.0 
        curTime=time()
        self.yaw=self.yaw+(Gz*(curTime-self.prevTime))*(360/48)

        if prevRes<360 and self.yaw>360:
            self.yaw=self.yaw-360
        elif prevRes>0 and self.yaw<0:
            self.yaw=self.yaw+360
        self.prevTime=curTime
        prevRes=self.yaw
        return self.yaw

    def getAngles(self):
		while True:
			Ax,Ay,Az=self.getAccel()
			Gx,Gz,Gz=self.getGyro()
	        
			pitch=self.get_x_rotation(Ax,Ay,Az)
			roll=self.get_y_rotation(Ax,Ay,Az)    
			return roll,pitch
			  
              

''' 
MPU_Init()
 
print (" Reading Data of Gyroscope and Accelerometer")

while True:
     
    #Read Accelerometer raw value
 
     
 
    print ("Gx=%.2f" %Gx, "Gy=%.2f" %Gy, "Gz=%.2f" %Gz, "Ax=%.2f g" %Ax, "Ay=%.2f g" %Ay, "Az=%.2f g" %Az)     
    sleep(0.6)
'''
