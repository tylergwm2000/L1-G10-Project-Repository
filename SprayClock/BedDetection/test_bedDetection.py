import bedDetection
import os
import shutil
import pytest
from time import sleep
from camera import Camera
from hx711 import HX711

db = bedDetection.initFirebase()
camera = Camera.init_camera()
hx = HX711(5,6)

#Test if camera works
def test_camera():
	if (os.path.isdir("images")):
		shutil.rmtree("images")
	os.mkdir("images")
	Camera.take_image(camera, "images/sample.jpg")
	assert os.path.exists("images/sample.jpg") == 1
	shutil.rmtree("images")

#Test if detecting from load sensor works
def test_bedDetection_loadSensor():
	bedWeight = hx.get_grams()
	hx.power_down()
	sleep(0.001)
	hx.power_up()
	assert False == bedDetection.loadDetection(hx, bedWeight) #Check loadDetection method returns False when no change in weight
	assert True == bedDetection.loadDetection(hx, -100) #Check loadDetection method returns True when bedWeight is -100

#Test if detecting from camera works
def test_bedDetection_camera():
	assert True == Camera.camera_detection("test_images/sample.jpg", "Google_MSCOCO_Model/detect.tflite", "Google_MSCOCO_Model/labelmap.txt") #Check if picture taken with person returns True
	assert False == Camera.camera_detection("test_images/sample1.jpg", "Google_MSCOCO_Model/detect.tflite", "Google_MSCOCO_Model/labelmap.txt") #Check if picture taken with no person returns false
	assert True == Camera.camera_detection("test_images/sample2.jpg", "Google_MSCOCO_Model/detect.tflite", "Google_MSCOCO_Model/labelmap.txt")
	assert True == Camera.camera_detection("test_images/sample3.jpg", "Google_MSCOCO_Model/detect.tflite", "Google_MSCOCO_Model/labelmap.txt")
	assert True == Camera.camera_detection("test_images/sample4.jpg", "Google_MSCOCO_Model/detect.tflite", "Google_MSCOCO_Model/labelmap.txt")
	assert True == Camera.camera_detection("test_images/sample5.jpg", "Google_MSCOCO_Model/detect.tflite", "Google_MSCOCO_Model/labelmap.txt")
