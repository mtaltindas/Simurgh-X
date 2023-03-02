import os
import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("localhost",9999))
with open("simurgh.jpg","rb") as file:
	file_size=os.path.getsize("simurgh.jpg")
	print(file_size)

client.send("recieved_image.jpg".encode())
client.send(str(file_size).encode())
with open("simurgh.jpg","rb") as file:
	data=file.read()
client.sendall(data)
client.send(b"<END>")

file.close()
client.close()
