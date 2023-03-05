import smbus           
from time import sleep         


bus=smbus.SMBus(1)
address=0x1E

def bearingX():
	bear1=bus.read_byte_data(address,3)
	bear2=bus.read_byte_data(address,4)
	bear=(bear1<<8)+bear2
	return bear

def bearingY():
	bear1=bus.read_byte_data(address,7)
	bear2=bus.read_byte_data(address,8)
	bear=(bear1<<8)+bear2
	return bear

def bearingZ():
	bear1=bus.read_byte_data(address,5)
	bear2=bus.read_byte_data(address,6)
	bear=(bear1<<8)+bear2
	return bear

def setDefault():
	bus.write_byte_data(address,2,0)

while True:
	setDefault()
	sleep(0.07)
	x=bearingX()
	y=bearingY()
	z=bearingZ()
	print(x,"&&",y,"&&",z)
	sleep(0.2)

