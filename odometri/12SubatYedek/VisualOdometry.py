import numpy as np
import cv2
import time
from lib.flow import simurgh_flow
from lib.feature import simurgh_feature

###
###     TODO: Mavsdk//GY271 den drone un heading bilgisi alınacak?
###     TODO: HMC5883L/QMC5883 3 Eksen Pusula Sensörü - GY-271

import asyncio
from mavsdk import System


def simurgh_VO():
    
    trajectories = []
    frame_idx = 0
    cap = cv2.VideoCapture("./ImageProcess/5meter.mp4")
    avg_flowX2=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    avg_flowY2=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(avg_flowY2) 
    firstStartFlag=True
    while True:
        pts = np.array([[avg_flowX2-200, avg_flowY2], [avg_flowX2, avg_flowY2+200],[avg_flowX2+200, avg_flowY2], [avg_flowX2, avg_flowY2-200]],np.int32) 
        pts = pts.reshape((-1, 1, 2)) 

        start = time.time()
        
        suc, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = frame.copy()
        img = cv2.polylines(img, [pts],True, (0, 0, 0), 4)

        # Calculate optical flow for a sparse feature set using the iterative Lucas-Kanade Method
        if len(trajectories) > 0:
            if(firstStartFlag):
                #new_trajectories,avg_flowX2,avg_flowY2=simurgh_flow(frame_gray,prev_gray,trajectories,img,start,avg_flowX2,avg_flowY2,firstStartFlag)
                new_trajectories=simurgh_flow(frame_gray,prev_gray,trajectories,img,start,avg_flowX2,avg_flowY2,firstStartFlag)
               
                firstStartFlag=False
            else:    
                #new_trajectories,avg_flowX2,avg_flowY2=simurgh_flow(frame_gray,prev_gray,trajectories,img,start,avg_flowX2,avg_flowY2,firstStartFlag)
                new_trajectories=simurgh_flow(frame_gray,prev_gray,trajectories,img,start,avg_flowX2,avg_flowY2,firstStartFlag)
            trajectories = new_trajectories 
              
            # Tespit edilen ozniteliklerin egrisi ciziliyor.
            cv2.polylines(img, [np.int32(trajectory) for trajectory in trajectories], False, (0, 255, 0))
            cv2.putText(img, 'track count: %d' % len(trajectories), (20, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2)


        # Belirlenen aralığa göre tekrar oznitelik tespiti yapiyor.
        if frame_idx % fps == 0:
            mask,trajectories=simurgh_feature(frame_gray,trajectories)

        frame_idx += 1
        prev_gray = frame_gray
        #im1 = cv2.resize(img, (960, 540))   

        cv2.imshow('Optical Flow', img)
        #cv2.imshow('Mask', im2)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()
simurgh_VO()
