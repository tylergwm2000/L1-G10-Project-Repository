import bedDetection
import os
import shutil
import pytest

db = bedDetection.init_firebase()

def test_bedDetection_loadSensor():
	assert bedDetection.loadDetection() == True #Check loadDetection method returns true
	data = db.child("Subsystem Status").child("Bed Detection").child("Load Sensor").get() #Get value for Load Sensor from Firebase
	assert data.val() == bedDetection.loadDetection() #Check if value from Firebase is same as loadDetection method (True)

def test_bedDetection_camera():
	camera = bedDetection.init_camera()
	if (os.path.isdir("images")):
		shutil.rmtree("images")
	os.mkdir("images")
	camera.capture("images/background.jpg")
	data = db.child("Subsystem Status").child("Bed Detection").child("Camera").get() #Get value for Camera from Firebasse
	assert data.val() == bedDetection.cameraDetection(camera, "images/background.jpg") #Check if value from Firebase is the same as cameraDetection method 
	shutil.rmtree("images")
