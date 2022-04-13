# SprayClock
![alt text](https://github.com/tylergwm2000/L1-G10-Project-Repository/blob/main/images/SprayClock.jpg)
---
#### Team Members: Tyler Mak, Leenesh Kumar, Celeste McCaffrey
#### Group: L1-G10W
#### TA Name: Victoria Ajila
#### Course Code: SYSC3010A
---
## Project Summary  
![alt text](https://github.com/tylergwm2000/L1-G10-Project-Repository/blob/main/images/DeploymentDiagram.png)  
Alarm clocks are used around the world to help individuals keep track of time and to plan schedules for upcoming events. They have evolved throughout different eras to suit the needs of people who prefer the latest technology in their devices. One common problem however, is that people are not able to keep track of their sleep and see if they are undersleeping or oversleeping. The SprayClock will help individuals get their sleep schedules back on track by ensuring that they get their desired amount of sleep and prevent oversleeping by spraying water on people who are still in bed after their alarm goes off. The user will have the ability to check their sleep pattern on a website which will chart data from the past week or month. The website will also be the interface the user uses to set alarms, delete alarms, and check what alarms have been set. 

In the image shown above, is a UML deployment diagram that describes our system and how it has been broken up into its respective subsystems. In this project, we will have a subsystem for our spray mechanism, a subsystem for our alarm, and a subsystem for bed detection. All of these subsystems will have a means to communicate to the Realtime Firebase database which will store all information received and use it to produce a graph on the Web GUI.

---
### Repository Directory Structure
The entire project is located in the SprayClock folder.  

    .
    ├── Lab 4                   # Folder corresponding to Lab 4 work 
    ├── SprayClock              # SprayClock Project Folder
    │   ├── Alarm               # Alarm Clock Subsystem Folder
    │   │   ├── install_Alarm.sh               # Bash script to install libraries for Alarm subsystem
    │   │   ├── lcd.py                         # LCD Screen code
    │   │   ├── main.py                        # Alarm Clock code
    │   │   └── test_alarm.py                  # Alarm Clock test program
    │   ├── Bed Detection       # Bed Detection Subsystem Folder
    │   │   ├── GOOGLE_MSCOCO_Model            # TensorFlow Lite Model
    │   │   ├── test_images                    # Test images for test cases
    │   │   ├── bedDetection.py                # Bed Detection code
    │   │   ├── camera.py                      # Camera code
    │   │   ├── hx711.py                       # Load Sensor code
    │   │   ├── install_BedDetection.sh        # Bash script to install libraries for Bed Detection subsystem
    │   │   ├── testLoadSensor.py              # Load Sensor test program
    │   │   └── test_bedDetection.py           # Bed Detection test program
    │   ├── Spray               # Spray Subsystem Folder
    │   │   ├── backend.py                     # Website backend code
    │   │   ├── frontend.py                    # Website frontend code
    │   │   ├── install_Spray.sh               # Bash script to install libraries for Spray subsystem
    │   │   ├── sprayStepperMotor.py           # Spray code
    │   │   ├── test_Web_GUI.py                # Web GUI test program
    │   │   └── test_sprayTest.py              # Spray test program
    │   └── install.sh          # Bash script to install all necessary libraries for entire system  
    ├── WeeklyUpdates           # Folder containing WIPURs for each group member each week  
    ├── images                  # Folder containing images for README.md file
    └── README.md

---
## Necessary Hardware  
The SprayClock project will use the following hardware:  

The Bed Detection Subsystem will use:  
- A Raspberry Pi 4
- Raspberry Pi Camera v2 
- HX711 Breakout Board
- Load Cell  
The wiring for the Bed Detection Subsystem is as follows:  
![alt text](https://github.com/tylergwm2000/L1-G10-Project-Repository/blob/main/images/BedDetectionWiring.png)  

The Alarm Clock Subsystem will use:  
- A Raspberry Pi 4
- Push Button
- Active Buzzer
- 16x2 LCD Screen
- 10k Potentiometer  
The wiring for the Alarm Clock Subsystem is as follows:  
![alt text](https://github.com/tylergwm2000/L1-G10-Project-Repository/blob/main/images/AlarmClockWiring.png)  

The Spray Subsystem will use:  
- A Raspberry Pi 4
- ULN2003 Stepper Motor Driver Board
- 28BYJ-48 5V Stepper Motor  
The wiring for the Spray Subsystem is as follows:  
![alt text](https://github.com/tylergwm2000/L1-G10-Project-Repository/blob/main/images/SprayWiring.png)  
---
## Installation Instructions  
Each subsystem will require different libraries to be installed. If you don't mind installing all necessary libraries for the entire system you can run the bash script install.sh in the SprayClock folder using the command `./install.sh`. The instructions to install each subsystem's libraries separately will be shown below.  
### Bed Detection Subsystem
The Bed Detection Subsystem will need the Pyrebase4, Virtual Environment, TensorFlow Lite and OpenCV libraries.  
Open the terminal and follow the instructions below. 
If you haven't already enable the Raspberry Pi Camera by typing `sudo raspi-config`
Once the Software Configuration Tool shows up, navigate to Interface Options then select the Legacy Camera Enable/Disable.
Before any installation, if you haven't already run the commands:
```
sudo apt-get update  
sudo apt-get upgrade
```
Now to install Pyrebase4 & Virtual Environment type the commands:  
```
python -m pip install pyrebase4
pip3 install virtualenv
```
To ensure no conflicts occur for the installation of the following libraries create and start the virtual environment with the following commands:
```
python3 -m venv name-of-environment          # Use a name you think fits the occasion Ex. BedDetection
source name-of-environment/bin/activate 
```
If the environment was to ever be deactivated rerunning the `source name-of-environment/bin/activate` command will reactivate it.
This environment will need to be activated to run any of the Bed Detection code.
With the environment activated the terminal should look as follows: `(name-of-environment)pi@raspberrypi: ~$ `  
Now you can either run the command `./install_BedDetection.sh` or follow the remaining instructions below.  
Next is to install OpenCV using the following commands:  
```
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev 
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libatlas-base-dev
pip3 install opencv-python==4.5.3.56
```
The final step is to install TensorFlow Lite, first check which version of Python you are using with `python3 --version` then run the command in the table below:
| Python Version | Command to Issue           |
| ------------- |:-------------:| 
| 3.9      | `pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp39-cp39-linux_armv7l.whl` | 
| 3.8      | `pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp38-cp38-linux_armv7l.whl` | 
| 3.7      | `pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp37-cp37m-linux_armv7l.whl` | 
| 3.6      | `pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp36-cp36m-linux_armv7l.whl` | 
| 3.5      | `pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp35-cp35m-linux_armv7l.whl` |  

After running the above command install the last package with the following command:  
```
python3 -m pip install tflite-support>=0.3.1
```
If no errors occured, you have successfully installed all necessary libraries & packages for the Bed Detection Subsystem.  
### Alarm Clock Subsystem
The Alarm Clock Subsystem will need pyrebase, time, datetime, RPI.GPIO libraries

Note that many of these libraries may already be installed on your RPi. However in the case that they are not, you can use the bash script through the command `./install_Alarm.sh` or through the following commands:
```
sudo apt-get update //This will be helpful to make sure that all files and software is updated

sudo apt-get upgrade // Will be good if you would like to upgrade the software version on your RPi

python -m pip install pyrebase //You can use this to install the pyrebase library in you RPi, crucial to configure a connection to Realtime Firebase database from your python file

python -m pip install time //This is used to install the time library in your RPi, crucial to set time of a particular format.

python -m pip install datetime //This is used to install the datetime library in your RPi, crucial to get current date and time from real world to show in your clock

python -m pip install RPI.GPIO//This is used to install the RPI.GPIO library in your RPi, crucial for linking the GPIO pin numbers from your hardware to software
```

### Spray Subsystem

### a. Stepper Motor
The Spray Subsystem will need pyrebase, time, and RPI.GPIO libraries. It is also good practice to ensure your RPi is updated and has been upgraded if possible. Many of these libraries may already be installed on your RPi. However, to ensure these files are installed, please run through the commands below:
```
sudo apt-get update //ensuring all files and software is updated
sudo apt-get upgrade //check on upgrade the software version on your RPi
python -m pip install pyrebase // realtime Firebase database
python -m pip install time // installing the time library in your RPi
python -m pip install RPI.GPIO//installing the RPI.GPIO library in your RPi
```

### b. Web GUI
The Web GUI will be hosted off of the Spray subsystem. So the following libraries will need to be installed on the Spray RPi: pyrebase, dash libraries, and pandas libraries.
To install these libraries use the bash script through the command `./install_Spray.sh` or enter the following commands:
```
python -m pip install pyrebase4
sudo apt-get install python3-numpy 
sudo apt-get install python3-pandas
pip3 install pyrebase4 dash dash_daq dash-extensions coloredlogs
```
---
## How to run the system  
In order to run the entire system the following files will need to be run in each subsystem.

### Bed Detection Subsystem
For the Raspberry Pi running the Bed Detection Subsystem, the bedDetection.py file must be run using the following command:
```
python3 bedDetection.py
```
Once the command has been run and all wire connections and extra hardware is properly connected to the system, the program should show the following output.  
It will first ask the user to calibrate the load sensor, after which the program will begin operating and will constantly check the load sensor and the camera inputs for person to be in bed. 

![alt text](https://github.com/tylergwm2000/L1-G10-Project-Repository/blob/main/images/BedDetectionOutput1.png)  
![alt text](https://github.com/tylergwm2000/L1-G10-Project-Repository/blob/main/images/BedDetectionOutput2.png)  

### Alarm Clock Subsystem
To run the AlarmClock Subsystem, the main.py and the lcd.py in the Alarm folder must be run using the following commands:
```
python3 main.py
python3 lcd.py
```
In theory it should work. However, for some reason the program causing the RPi to lose connection.

### Spray Subsystem
In order to run the Spray Subsystem, the sprayStepperMotor.py file must be run using the following command:
```
python3 sprayStepperMotor.py
```
Once this command is run, the Spray Subsystem will be consistently checking in an infinite loop if the spray is activated or deactivated based on the user’s alarms.

### Web GUI
In order to run the Web GUI, the frontend.py file must be run using the following command:
```
python3 frontend.py
```
Once this command has been run, the Web GUI will begin running and you should be able to go to the website on any device connected to your home network through the following url:  
Spray RPi IP Address:8050  Ex. 192.168.0.1:8050  
The website should look as follows: 
![alt text](https://github.com/tylergwm2000/L1-G10-Project-Repository/blob/main/images/Website.png) 

---
