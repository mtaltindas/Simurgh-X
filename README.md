

# *Autonomous Quadcopter Project for TEKNOFEST UAV 2023 Competition*


---
## Description

<p align="center">
<img src="simurghLogo.png"  width="558" height="470">
<img src="huuav.png" width="470" height="558">
</p>


*will be implemented at a later time*

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

---
## ***Raspberry Pi HQ Camera***

[RPI HQ LINK1](
 https://www.hackster.io/SaadTiwana/embedded-diaries-how-to-use-rpi-hq-camera-with-jetson-e2063e)

[RPI HQ LINK2](https://github.com/RidgeRun/NVIDIA-Jetson-IMX477-RPIV3)

[RPI HQ LINK3](https://developer.ridgerun.com/wiki/index.php?title=Raspberry_Pi_HQ_camera_IMX477_Linux_driver_for_Jetson#Installing_the_Driver_-_Option_A:_Debian_Packages_.28Recommended.29) 

[SCP Command Problem](https://unix.stackexchange.com/questions/47909/transfer-files-using-scp-permission-denied)
```
camSet='nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
```
---
## ***Jetson Nano URLS***

[VNC](https://developer.nvidia.com/embedded/learn/tutorials/vnc-setup)

[Jetson Pixhawk Cube  Connection](https://www.hackster.io/Matchstic/connecting-pixhawk-to-raspberry-pi-and-nvidia-jetson-b263a7)

[Upgrade Python Version on Jetson Nano](https://stackoverflow.com/questions/60824700/how-to-install-python3-9-on-linux-ubuntu-terminal)


[PIP Error](https://stackoverflow.com/questions/44967202/pip-is-showing-error-lsb-release-a-returned-non-zero-exit-status-1)

---
 

## ***PCA9685 Servo Control:***
- [Adafruit LIB](https://github.com/adafruit/Adafruit_Python_PCA9685)
- [Youtube Tutorial](https://www.youtube.com/watch?v=D2gSvXo0qT8)
- [Another LIB for PCA9685](https://github.com/adafruit/Adafruit_CircuitPython_PCA9685)

## ***BMP180:*** 

[Press Sensor 101](https://learn.sparkfun.com/tutorials/bmp180-barometric-pressure-sensor-hookup-/all)

[Press Sensor 101-2](https://how2electronics.com/bmp180-altitude-pressure-temperature-measurement/)

## ***MPU6050:***
[Sensor Usage](https://automaticaddison.com/visualize-imu-data-using-the-mpu6050-ros-and-jetson-nano/)

## ***HMC5883L:***
[Link1](https://blog.csdn.net/ManWZD/article/details/103147985)

[Sensor Usage](https://www.instructables.com/Configure-read-data-calibrate-the-HMC5883L-digital/)
