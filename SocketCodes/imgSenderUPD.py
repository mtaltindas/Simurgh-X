import random
import socket, select
from time import gmtime, strftime,sleep
from random import randint
import os

class sendpackage:
	def __init__(self):
		self.image = "simurgh.jpg"

		self.HOST = '10.225.133.252'
		self.PORT = 6666

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (self.HOST, self.PORT)
		
	def sendEnemy(self):
		try:
			self.sock.connect(self.server_address)
			file = open(self.image, 'rb')
			file_size=os.path.getsize(self.image)
			size_msg=("SIZE "+str(file_size))
			print(size_msg)
			self.sock.send(size_msg.encode())
			answer = self.sock.recv(1024).decode()
			print (answer)

			if answer == 'Dosya boyutu gonderildi':

				data=file.read()
				self.sock.sendall(data)
				answer = self.sock.recv(1024).decode()
				
				if answer == 'Resim gonderildi' :
					print (answer)
				file.close()
				self.sock.close()
		except:
			print("HATA")

enemy=sendpackage()
enemy.sendEnemy()
	
