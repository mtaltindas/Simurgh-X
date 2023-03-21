import cv2 
import numpy as np
from clientUPDFinal import *
#from simurgh_servo import *


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
    cap = cv2.VideoCapture("./12SubatYedek/c.avi")
    redval=0
    blueval=0
    enemyFlag=False
    allyFlag=False
    #client=package()
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
                        if redval>100:
                            #DUSMAN KODUNU CALISTIR
                            print("red val limit reached")
                            filename = 'Dusman.png'
                            cv2.imwrite(filename, frame)
                            #client.send_Enemy()
                            enemyFlag=True
                            redval=-1000000000
                            print("DUSMAN RESMI TESPIT EDILDI,GONDERILDI")
                        
                        
                    elif name=="blue":
                        blueval+=1
                        if blueval>100:
                            #SERVOYU CALISTIR
                            #servo.releaseSupplyKit()
                            print("blue val limit reached")

                            allyFlag=True
                            blueval=-1000000000
                            print("DOST ASKERLERINE YARDIM PAKETI GONDERILDI")
                        
                cv2.imshow('frame', frame)
            
            if (cv2.waitKey(10) & (0xFF == ord('q'))) or (enemyFlag and allyFlag) :
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

missionOneIP()