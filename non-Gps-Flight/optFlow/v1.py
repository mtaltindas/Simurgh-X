import numpy as np
import cv2
import time
from lib.flow import simurgh_flow
from lib.feature import simurgh_feature

###
###     TODO: Mavsdk dan drone un heading bilgisi alınacak?
###
import asyncio
from mavsdk import System

trajectory_len = 1000
detect_interval = 15
trajectories = []
frame_idx = 0
cap = cv2.VideoCapture("./opticalFlow/1.mp4")

while True:

    start = time.time()

    suc, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = frame.copy()

    # Calculate optical flow for a sparse feature set using the iterative Lucas-Kanade Method
    if len(trajectories) > 0:

        new_trajectories,estimatedLocation=simurgh_flow(frame_gray=frame_gray,prev_gray=prev_gray,trajectories=trajectories,img=img,startTime=start)
        ##
        ##  TODO: Güncel konum otopilota burada iletilecek  ####
        ##
        trajectories = new_trajectories 
            
        # Draw all the trajectories
        cv2.polylines(img, [np.int32(trajectory) for trajectory in trajectories], False, (0, 255, 0))
        cv2.putText(img, 'track count: %d' % len(trajectories), (20, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2)


    # Update interval - When to update and detect new features
    if frame_idx % detect_interval == 0:
        mask,trajectories=simurgh_feature(frame_gray,trajectories)

    frame_idx += 1
    prev_gray = frame_gray


    
    
    cv2.imshow('Optical Flow', img)
    #cv2.imshow('Mask', mask)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
