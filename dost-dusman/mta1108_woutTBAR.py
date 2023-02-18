#Contours olayi opencv 4 icin calisiyor(2 parametre)

import cv2
import numpy as np
import imutils

#vid=cv2.VideoCapture(0)
vid = cv2.VideoCapture("./ImageProcess/b.avi")


#pts = np.array([[70,200],[70,410],[275,410],[275,200]], np.int32)
#pts2=np.array([[w/2-(w/6),h/2-(h/6)],  [w/2-(w/6),h/2+(h/6)],    [w/2+(w/6),h/2+(h/6)],  [w/2+(w/6),h/2-(h/6)]], np.int32)
                # sol üst  (x,y)         ,   sol alt,                   sağ alt,                 sağ üst

pts2=np.array([[100,180],   [100,350],  [250,350],  [250,180]], np.int32)

#array range for the outside
#lower_red = np.array([0,100,150])
#upper_red = np.array([12,255,255])

#array range for the inside
lower_red = np.array([135,120,120])
upper_red = np.array([179,255,255])

kernelOpen=np.ones((6,6),np.uint8)
kernelClose=np.ones((4,4),np.uint8)
kernel = np.ones((9,9),np.uint8)

def get_cnts(frame):
    #This functions purpouse is process the raw image & return the contours of the red circle if any find
    blurred_frame=cv2.GaussianBlur(frame,(13,13),cv2.BORDER_DEFAULT)
    hsv=cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(hsv,lower_red,upper_red)
    ret,thresh=cv2.threshold(mask,50,252,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #Dilation is important for preventing mistaken areas(noises) but im not so sure about threshold & other morph op's

    dilatedmask = cv2.dilate(thresh,kernel,iterations = 4)
    maskOpen=cv2.morphologyEx(dilatedmask,cv2.MORPH_OPEN,kernelOpen)             
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    cv2.imshow("bbb",dilatedmask)
    cv2.imshow("bcb",maskOpen)
    cv2.imshow("bdb",maskClose)

    items=cv2.findContours(dilatedmask,0 ,1)
    cnts=imutils.grab_contours(items)
    return cnts
    

def findCenter(frame,contour):
    M=cv2.moments(contour)
    cX=int(M["m10"]/M["m00"])
    cY=int(M["m01"]/M["m00"])
    area=cv2.contourArea(contour)
    pts = pts2.reshape((-1,1,2))
    cv2.polylines(frame,[pts],True,(0,255,0),5)
    cv2.putText(frame,"Selenga-DK ",(0,20),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),2)
    if area>15000:
        #TODO:Is approx method necessary? 
        #TODO:maybe you can check the perimeter of the circle to ensure the correctness??
        #approx=cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        #x=approx.ravel()[0]
        #y=approx.ravel()[1]
        #print(str(cX)+" "+str(cY))
        if(cY<350 and cY>180 and cX<250 and cX>150):
            cv2.circle(frame,(cX,cY),15,(0,0,0),-1)
            cv2.putText(frame,"Getting location data..",(0,630),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),2)
            cv2.putText(frame,"Selenga-DK ",(0,20),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),2)

            cv2.drawContours(frame,contour,-1, (0, 0, 0),3)
            # TODO:!!!LOCATION DATA WILL BE USED HERE!!!
        else:
            cv2.circle(frame,(cX,cY),15,(0,0,0),3)
            cv2.putText(frame,"The point is not in the middle.",(0,630),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),2)
            cv2.drawContours(frame,contour,-1, (0, 0, 0),3)



def main_Prog():
    if(vid.isOpened()==False):
        print("error")
    else:
        while (vid.isOpened()):
            ret,frame2=vid.read()


            cnts=get_cnts(frame2)
            for contour in cnts:
                findCenter(frame2,contour)
            
            
            print(vid.get(cv2.CAP_PROP_FPS))

            if ret==True:
                cv2.imshow("final",frame2)
                
                if cv2.waitKey(20) & 0xFF == ord('1'):
                    break
            else:
                break
    vid.release()
    cv2.destroyAllWindows()



            #cv2.imshow("thresh",thresh)
            #cv2.imshow("video",dilatedmask)
            #cv2.imshow("mask",maskOpen)
            #cv2.imshow("maskClose",maskClose)



main_Prog()