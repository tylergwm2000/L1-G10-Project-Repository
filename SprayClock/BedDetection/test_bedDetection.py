import bedDetection
import os
import shutil
import pytest
from camera import Camera
from hx711 import HX711

db = bedDetection.init_firebase()
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
	data = db.child("Subsystem Status").child("Bed Detection").child("Load Sensor").get() #Get value for Load Sensor from Firebase
	assert data.val() == bedDetection.loadDetection(hx, bedWeight) #Check if value from Firebase is same as loadDetection method

#Test if detecting from camera works
def test_bedDetection_camera():
	if (os.path.isdir("images")):
		shutil.rmtree("images")
	os.mkdir("images")
	Camera.take_image(camera, "images/sample.jpg")
	data = db.child("Subsystem Status").child("Bed Detection").child("Camera").get() #Get value for Camera from Firebasse
	assert data.val() == Camera.camera_detection("images/sample.jpg", "Google_MSCOCO_Model/detect.tflite", "Google_MSCOCO_Model/labelmap.txt") #Check if value from Firebase is the same as camera_detection method 
	shutil.rmtree("images")
