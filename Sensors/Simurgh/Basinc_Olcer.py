import smbus
import time
from ctypes import c_short
class bmp180Sensor: 
	def __init__(self,port,i2cAddress=0x77):
		self.DEVICE = i2cAddress
		self.bus = smbus.SMBus(port) 
		self.REG_CALIB  = 0xAA
		self.REG_MEAS   = 0xF4
		self.REG_MSB    = 0xF6
		self.REG_LSB    = 0xF7
		self.CRV_TEMP   = 0x2E
		self.CRV_PRES   = 0x34 
		self.OVERSAMPLE = 3  

		self.REG_ID     = 0xD0

		self.CalibOffset=900
		self.minOffset=0
		self.maxOffset=0
	def calibrate(self):
		print("Calibration Started")
		calibSum=0
		j=0
		dummy1,maxVal=self.readBmp180()
		dummy2,minVal=self.readBmp180()
		while(j<400):
			j+=1
			temp,press=self.readBmp180()
			if(press>maxVal):
				maxVal=press
			elif(press<minVal):
				minVal=press

			calibSum+=press
			time.sleep(0.1)

		self.CalibOffset,a=self.getAltitude(True,calibSum/j)
		print("<<<Calibration done>>>")
		print(self.CalibOffset)
		self.minOffset,b=self.getAltitude(True,minVal)
		self.maxOffset,c=self.getAltitude(True,maxVal)
	def getAltitude(self,readFlag,pressure=-1):
		i=20
		totalpressure=0
		pressList=[]
		while i>0:
			if readFlag:
				temp=-1
				return ((1-((pressure/1013.25)**(1/5.255)))*44330),temp
			else:
				temp,pressure=self.readBmp180()
				pressList.append(pressure)
				totalpressure+=pressure
				i-=1
			time.sleep(0.01)
		avgPressure=totalpressure/20
		
		i=0
		while i<len(pressList):
			if (pressList[i]-avgPressure>0.025) or (pressList[i]-avgPressure<-0.025):
				del pressList[i]
			i+=1
		sum=0
		for press in pressList:
			sum+=press
		avgSum=sum/len(pressList)
		pressure=avgSum
		return ((1-((pressure/1013.25)**(1/5.255)))*44330)-self.CalibOffset,temp

	def convertToString(self,data):
	
		return str((data[1] + (256 * data[0])) / 1.2)

	def getShort(self,data, index):
	
		return c_short((data[index] << 8) + data[index + 1]).value

	def getUshort(self,data, index):
		return (data[index] << 8) + data[index + 1]

	def readBmp180Id(self):
	
		(chip_id, chip_version) = self.bus.read_i2c_block_data(self.DEVICE, self.REG_ID, 2)

		return (chip_id, chip_version)
	
	def readBmp180(self):

	
		cal = self.bus.read_i2c_block_data(self.DEVICE, self.REG_CALIB, 22)

		AC1 = self.getShort(cal, 0)
		AC2 = self.getShort(cal, 2)
		AC3 = self.getShort(cal, 4)
		AC4 = self.getUshort(cal, 6)
		AC5 = self.getUshort(cal, 8)
		AC6 = self.getUshort(cal, 10)
		B1  = self.getShort(cal, 12)
		B2  = self.getShort(cal, 14)
		MB  = self.getShort(cal, 16)
		MC  = self.getShort(cal, 18)
		MD  = self.getShort(cal, 20)

		#Temp Reading
		self.bus.write_byte_data(self.DEVICE, self.REG_MEAS, self.CRV_TEMP)
		time.sleep(0.005)
		(msb, lsb) = self.bus.read_i2c_block_data(self.DEVICE, self.REG_MSB, 2)
		UT = (msb << 8) + lsb

		#Press. Reading
		self.bus.write_byte_data(self.DEVICE, self.REG_MEAS, self.CRV_PRES + (self.OVERSAMPLE << 6))
		time.sleep(0.04)
		(msb, lsb, xsb) = self.bus.read_i2c_block_data(self.DEVICE, self.REG_MSB, 3)
		UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - self.OVERSAMPLE)

		# Refine temperature
		X1 = ((UT - AC6) * AC5) >> 15
		X2 = (MC << 11) / (X1 + MD)
		B5 = X1 + X2
		temperature = (B5 + 8) >> 4

		# Refine pressure
		B6  = B5 - 4000
		B62 = B6 * B6 >> 12
		X1  = (B2 * B62) >> 11
		X2  = AC2 * B6 >> 11
		X3  = X1 + X2
		B3  = (((AC1 * 4 + X3) << self.OVERSAMPLE) + 2) >> 2

		X1 = AC3 * B6 >> 13
		X2 = (B1 * B62) >> 16
		X3 = ((X1 + X2) + 2) >> 2
		B4 = (AC4 * (X3 + 32768)) >> 15
		B7 = (UP - B3) * (50000 >> self.OVERSAMPLE)

		P = (B7 * 2) / B4

		X1 = (P >> 8) * (P >> 8)
		X1 = (X1 * 3038) >> 16
		X2 = (-7357 * P) >> 16
		pressure = P + ((X1 + X2 + 3791) >> 4)

		return (temperature/10.0,pressure/ 100.0)


'''    
  (chip_id, chip_version) = readBmp180Id()
  print ("Chip ID     :", chip_id)
  print ("Version     :", chip_version)

  
  while True:
  		(temperature,pressure)=readBmp180()
  		print ("Temperature : ", temperature, "C")
  		print ("Pressure    : ", pressure, "mbar")
		altitude=prestoaltitude(pressure)
		print ("Altitude    : ", altitude, "meter")
		time.sleep(1)
  
if __name__=="__main__":
   main()
'''
