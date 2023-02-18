import numpy as np
import cv2
import time

from lib.flow import *
from lib.feature import *




detect_interval = 15
trajectories = []
frame_idx = 0

j=0
cap = cv2.VideoCapture("./ImageProcess/b.avi")
avgDelPixel=0
totalpixelchange=0
#print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


while True:
    
    # start time to calculate FPS
    start = time.time()

    suc, frame = cap.read()
    if suc:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = frame.copy()
    #############################################FLOW
        # Calculate optical flow for a sparse feature set using the iterative Lucas-Kanade Method
        if len(trajectories) > 0:
            new_trajectories,img,avgDelPixel,j=simurgh_flow(prev_gray,frame_gray,trajectories,img,j,width,height)
            totalpixelchange+=avgDelPixel
    #############################################FLOW
            
            trajectories = new_trajectories 

            # Draw all the trajectories
            cv2.polylines(img, [np.int32(trajectory) for trajectory in trajectories], False, (0, 0, 0),2)
            cv2.putText(img, 'track count: %d' % len(trajectories), (20, 50),cv2.LINE_AA, 1, (0,255,0),2)


        # Update interval - When to update and detect new features
        if frame_idx % detect_interval == 0:
            simurgh_feature(frame_gray,trajectories)
            print("total pixel change>>",totalpixelchange)

        frame_idx += 1
        prev_gray = frame_gray

        # End time
        end = time.time()
        # calculate the FPS for current frame detection
    # fps = 1 / (end-start)
        
        # Show Results
    # cv2.putText(img, f"{fps:.2f} FPS", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #imS = cv2.resize(img, (width,height))   
        cv2.imshow('Optical Flow', img)
        #cv2.imshow('Mask', mask)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            avgDelPixel=simurgh_pixel_change(trajectories)
            totalpixelchange+=avgDelPixel
            print("final pixel change>>",totalpixelchange)
            break
    else:
        avgDelPixel=simurgh_pixel_change(trajectories)
        totalpixelchange+=avgDelPixel
        print("final pixel change>>",totalpixelchange)
        break

cap.release()
cv2.destroyAllWindows()
