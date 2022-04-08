#!/bin/bash

#Pyrebase4
python -m pip install pyrebase4

#Virtual Environment
pip3 install virtualenv

#OpenCV
sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install libatlas-base-dev
pip3 install opencv-python==4.5.3.56

#TensorFlow Lite
version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [ $version == "3.9" ]; then
pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp39-cp39-linux_armv7l.whl
fi

if [ $version == "3.8" ]; then
pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp38-cp38-linux_armv7l.whl
fi

if [ $version == "3.7" ]; then
pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp37-cp37m-linux_armv7l.whl
fi

if [ $version == "3.6" ]; then
pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp36-cp36m-linux_armv7l.whl
fi

if [ $version == "3.5" ]; then
pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp35-cp35m-linux_armv7l.whl
fi
python3 -m pip install tflite-support>=0.3.1

#Time & datetime
python -m pip install time
python -m pip install datetime

#RPi.GPIO
python -m pip install RPI.GPIO

#numpy & pandas
sudo apt-get install python3-numpy
sudo apt-get install python3-pandas

#Dash library
pip3 install dash
pip3 install dash_daq
pip3 install dash-extensions
pip3 install coloredlogs
