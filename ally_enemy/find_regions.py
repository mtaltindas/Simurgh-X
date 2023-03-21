import cv2 
import numpy as np
from imgSenderUPD import *
#from simurgh_servo import *
import time
def gstreamer_pipeline():
    sensor_id=0
    capture_width=1080
    capture_height=1920
    display_width=540
    display_height=960
    framerate=30
    flip_method=1
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def region_type(n):
    if n == 0:
        name = "blue"
        hsv_lower = (100, 100, 100)
        hsv_upper = (110, 255, 255)
        return (name, hsv_lower, hsv_upper)
    
    elif n == 1:
        name = "red"
        lower_red = np.array([0, 100, 20])
        upper_red = np.array([20, 255, 255])
        lower_red2 = np.array([150, 100, 20])
        upper_red2 = np.array([179, 255, 255])
        hsv_lower = np.array([lower_red, lower_red2])
        hsv_upper = np.array([upper_red, upper_red2])
        return (name, hsv_lower, hsv_upper)
def missionOneIP():
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    redval=0
    blueval=0
    enemyFlag=False
    allyFlag=False
    client=sendpackage()
    #servo=SimurghServo()
    while True:
        ret, frame = cap.read()
        if ret == True:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            for i in range(2):
                (name, hsv_lower, hsv_upper) = region_type(i) 
                if i == 0:
                    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
                elif i ==1:
                    mask1 = cv2.inRange(hsv, hsv_lower[0], hsv_upper[0])
                    mask2 = cv2.inRange(hsv, hsv_lower[1], hsv_upper[1])
                    mask = cv2.bitwise_or(mask1, mask2)
                    
                kernel = np.ones((3,3), np.uint8)
                mask = cv2.erode(mask, kernel, iterations=1)
                mask = cv2.dilate(mask, kernel, iterations=1)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                if len(contours)>0:
                    biggest = sorted(contours,key = cv2.contourArea,reverse=True)[0]
                    rect = cv2.boundingRect(biggest)
                    x,y,w,h = rect
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),2)
                    cv2.putText(frame, name, (x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)
                    if name=="red":
                        redval+=1
                        if redval>500:
                            #DUSMAN KODUNU CALISTIR
                            print("red val limit reached")
                            #filename = 'Dusman.png'
                            #cv2.imwrite(filename, frame)
                            #client.sendEnemy()
                            #time.sleep(10)
                            enemyFlag=True
                            redval=-1000000000
                            print("DUSMAN RESMI TESPIT EDILDI,GONDERILDI")
                        
                        
                    elif name=="blue":
                        blueval+=1
                        if blueval>500:
                            #SERVOYU CALISTIR
                            #servo.releaseSupplyKit()
                            print("blue val limit reached")
                            filename='Dusman.png'
                            cv2.imwrite(filename,frame)
                            client.sendEnemy()
                            time.sleep(5)
                            allyFlag=True
                            blueval=-1000000000
                            print("DOST ASKERLERINE YARDIM PAKETI GONDERILDI")
                        
                #cv2.imshow('frame', frame)
            
            if (cv2.waitKey(10) & (0xFF == ord('q'))) or (enemyFlag and allyFlag) :
                print("FINISHHH")
                cap.release()
                cv2.destroyAllWindows()
                break
        else:
            break

    

missionOneIP()
