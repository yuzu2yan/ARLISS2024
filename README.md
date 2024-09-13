# ARLISS2024
![release_date](https://img.shields.io/badge/release_date-Sep_2024-yellow)
[![python](https://img.shields.io/badge/python-v3.9.2-blue)](https://www.python.org/downloads/release/python-392/)
[![openCV](https://img.shields.io/badge/OpenCV-v4.7.0-blue)](https://docs.opencv.org/4.7.0/)
[![openCV](https://img.shields.io/badge/YOLO-v8-blue)]([https://docs.opencv.org/4.7.0/](https://github.com/ultralytics/ultralytics))  
[![python](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)](https://www.python.org/)
[![linux](https://img.shields.io/badge/-Linux-6C6694.svg?logo=linux&style=flat)](https://www.linux.org/)
[![raspberrypi](https://img.shields.io/badge/-Raspberry%20Pi-C51A4A.svg?logo=raspberry-pi&style=flat)](https://www.raspberrypi.com/)

This is a project of Team Astrum in ARLISS 2024. 

<img width="515" alt="CanSat" src="https://github.com/user-attachments/assets/aea198a7-5fca-4d17-ac7c-68875f1c2c5a">

## Mission  
The CanSat is released from the launched rocket and reaches the goal at 0 m after a soft landing.  

## Mission Sequence  
The CanSat is stowed in the rocket and launched. After being released from the rocket, it lands and heads for the red cone at the goal. Guidance up to 8m from the goal is provided by GPS and magnetic sensors, while the area near the goal is guided by image processing. If stuck, a return process is performed.  

<img width="396" alt="mission sequence" src="https://github.com/user-attachments/assets/632c9b8b-6756-41fa-82ad-d75f5778c44f">


## Success Criteria  

| | Statement | Methodology |
| ---- | ---- |---|
| Minimum Success |The parachute separates normally and the CanSat makes a soft landing without damage |Confirmation by visual inspection and log|
| Full Success | Reach 8 m from the goal |Confirmation by visual inspection and log|
| Extra Success | Achieving 0 distance goal |Confirmation by visual inspection and log|

## Features

- Shock-absorbing shaft mechanism

<img width="226" alt="shaft" src="https://github.com/user-attachments/assets/a13518f3-10a2-43e2-ba61-2cc8b3ba773f">

- Robust to steps and obstacles

<img width="118" alt="tire" src="https://github.com/user-attachments/assets/f91863ef-774e-43bf-b6ab-6560bfab2e04">

- Separation mechanism for immediate separation

<img width="123" alt="separation mechanism" src="https://github.com/user-attachments/assets/43f69043-e155-4e00-b558-5042a7a27d68">

- Adaptable to backlighting and darkness​

<img width="279" alt="clahe" src="https://github.com/user-attachments/assets/a34fa9ff-740e-4702-8a96-9879148bd8ee">

- Model: YOLOv8​→Enable fast and accurate detection with limited resources​

<img width="172" alt="yolo" src="https://github.com/user-attachments/assets/a18d0199-2c9a-4370-b878-715831afd9c0">


## Software Configuration
Language : Python 3.9.2  
OS       : Ubuntu 22.04   
OpenCV   : Ver.4.7.0 

## Hardware Configuration

Computer                   : Raspberry Pi Zero 2  
GPS                        : GYSFDMAXB  
9-axis sensor              : BNO055  
Barometric pressure sensor : BME280   
Camera                     : Raspberry Pi Camera Module  
Communicator               : IM920sL  

## System Configuration

<img width="600px" alt="system diagram" src="https://github.com/user-attachments/assets/c23e6706-451a-482b-90d0-bfe452169f48">


## Program Configuration
- main.py  
    Main program. Operates according to the flow of the mission sequence.
- logger.py  
    Define a log class. Create logs for each phase and error and output them in csv format.
- floating.py  
    Used to calculate altitude; obtains air pressure and temperature from the BME280 module and calculates the altitude relative to the initial altitude.
- ground.py  
    This program is used in the ground phase. It calculates the distance and angle to the goal based on geomagnetic and GPS information, and determines the control.
- bme280.py  
    Obtain air pressure and temperature data using BME280.
- gnss.py  
    Obtains latitude and longitude from a GPS module every second. The acquisition program runs as a daemon.
- bno055.py  
    Obtain barometric pressure and acceleration data from BNO055. Each value is automatically calibrated by the built-in microcomputer, and the degree of calibration can be checked.
- cone_detection.py    
    It is an image processing module that takes a picture and detects red pylons in real time from the image.
- chat.py  
    Interact with the arm via ROS topic communication.
- motor.py  
    This class deals with motors, controlling tires and deployment motors.

## Result
The truck happened to land at the sample collection point, and the arm also collected the sample and even approached the truck.


However, the vibration of the movement during loading caused the sample to drop, and the mission was retired. The truck also failed to make a soft landing, damaging a tire upon landing.


**This mission won third place in the Tanegashima Rocket Contest2024!!**
