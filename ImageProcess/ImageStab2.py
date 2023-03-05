##
##  ROI EKLE
##  IMU ILE ROIYI DUZENLE
# Import numpy and OpenCV
import numpy as np
import cv2

import os
import sys
import time
import smbus
import math

from imusensor.MPU9250 import MPU9250


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1080,
    capture_height=1920,
    display_width=540,
    display_height=960,
    framerate=30,
    flip_method=0,
):
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


address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
imu.loadCalibDataFromFile("/home/simurgh/Codes/calib.json")
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=3), cv2.CAP_GSTREAMER)
	 
# Get frame count
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
fps=n_frames
# Get width and height of video stream
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
x_left=w*0.2
y_up=h*0.2
x_right=w*0.85
y_down=h*0.85
imu.readSensor()
imu.computeOrientation()
prevPitchAngle=imu.pitch
while True:

    imu.readSensor()
    imu.computeOrientation()
    pitchAngle=imu.pitch
    angleDiff=pitchAngle-prevPitchAngle
    if not((y_down-angleDiff*10)>h) or not(y_up<0):
        y_down-=angleDiff*10
        y_up-=angleDiff*10
    _, prev = cap.read() 
    # Convert frame to grayscale
    if not _:
        break
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    ROI= np.array([[(x_left,y_up),(x_right,y_up),(x_right,y_down),(x_left,y_down)]], dtype= np.int32)
  
    
    blank= np.zeros_like(prev_gray)
    region_of_interest= cv2.fillPoly(blank, ROI,255)

    region_of_interest_image= cv2.bitwise_and(prev_gray, region_of_interest)

    #imS = cv2.resize(region_of_interest_image, (int(3/5*int(w)),int(3/5*int(h))))  
    cv2.imshow('Region of Interest', region_of_interest_image)
        
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
