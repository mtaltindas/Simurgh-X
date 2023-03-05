##
##  ROI EKLE
##  IMU ILE ROIYI DUZENLE
# Import numpy and OpenCV
import numpy as np
import cv2

cap = cv2.VideoCapture('./5meter2.mp4')
 
# Get frame count
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
fps=n_frames
# Get width and height of video stream
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
x_left=w*0.1
y_up=h*0.1
x_right=w*0.9
y_down=h*0.9
while True:
    _, prev = cap.read() 
    # Convert frame to grayscale
    if not _:
        break
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    ROI= np.array([[(x_left,y_up),(x_right,y_up),(x_right,y_down),(x_left,y_down)]], dtype= np.int32)
  
    
    blank= np.zeros_like(prev_gray)
    region_of_interest= cv2.fillPoly(blank, ROI,255)

    region_of_interest_image= cv2.bitwise_and(prev_gray, region_of_interest)

    imS = cv2.resize(region_of_interest_image, (int(3/5*int(w)),int(3/5*int(h))))  
    cv2.imshow('Region of Interest', imS)
        
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
