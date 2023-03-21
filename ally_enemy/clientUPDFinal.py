
import socket
import tqdm




class package:
    def __init__(self):
        self.basename = "socket/Dusman.png"

        self.HOST = ''
        self.PORT = 6666
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        self.buffer_size = 1024

        self.sockfd, client_address = self.server_socket.accept()
        
        self.full_msg=b""
        print("Client Initialized")

    def getSize(self,txt):
        tmp = txt.split()
        
        size = int(tmp[1])
        return size

    def send_Enemy(self):
        try:
            print ('Paket buyuklugu>>', self.buffer_size)
            data = self.sockfd.recv(self.buffer_size).decode()
            txt = str(data)
            print(txt)
            if txt.startswith('SIZE'):
                
                size=self.getSize(txt)
                count=int(size)/1024+1
                print ('Dosya boyutu alindi')
                print ('Dosya boyutu>>',size)
                msg="Dosya boyutu gonderildi"
                self.sockfd.send(msg.encode())
                # Now set the buffer size for the image 
                
                file = open(self.basename, 'wb')

                progress=tqdm.tqdm(unit="B",unit_scale=True,unit_divisor=1000,total=int(size))
                while count>0:
                    data=self.sockfd.recv(1024)
                    self.full_msg+=data
                    count-=1
                    progress.update(1024)
                    
                file.write(self.full_msg)
                file.close()  
        
                end_msg="Resim gonderildi"
                self.sockfd.send(end_msg.encode())
                print(end_msg)
                    
        except:
            print("HATA")

        self.sockfd.close()
        self.server_socket.close() 






