#bedDetection.py implements Bed Detection Subsystem and uses the Load Cell and RPi camera
#Import required libraries
import pyrebase
from picamera import PiCamera
from hx711 import HX711
import RPi.GPIO as GPIO
from time import sleep
import os
import shutil
from datetime import datetime
from PIL import Image
import numpy as np

def init_camera():
	camera = PiCamera()
	return camera

#def init_loadSensor():
	#dout_pin = 23
	#pd_sck_pin = 24
	#hx711 = HX711(dout_pin, pd_sck_pin)
	#return hx711

def init_firebase():
	config = {
		"apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
		"authDomain": "sprayclock-4e902.firebaseapp.com",
		"databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
		"storageBucket": "sprayclock-4e902.appspot.com"}
	firebase = pyrebase.initialize_app(config)
	db = firebase.database()
	return db

#def loadDetection(hx, bedWeight):
	#current = hx._read()
	#difference = current - bedWeight
	#if difference > 0:
	#	print(difference)
	#	return True
	#else:
	#	return False
def loadDetection():
	return True

def cameraDetection(camera, background):
	imagefile = "images/{}.jpg".format(datetime.now().isoformat(timespec='minutes'))
	camera.capture(imagefile)
	image1 = Image.open(background)
	image2 = Image.open(imagefile)
	array1 = np.asarray(image1)
	array2 = np.asarray(image2)
	array3 = array2 - array1
	array3 = np.absolute(array3)
	sum = array3.sum()
	if sum > 480000000:
		print(sum)
		return True
	else:
		print(sum)
		return False

def main():
	try:
		db = init_firebase()
		camera = init_camera()
		#hx = init_loadSensor()
		if os.path.isdir("images"):
			shutil.rmtree("images")
		os.mkdir("images")
		parent = "Subsystem Status"
		subsystem = "Bed Detection"
		camera.capture("images/background.jpg")
		#bedWeight = hx._read()
		while (True):
			data = {"Camera": cameraDetection(camera, "images/background.jpg"), "Load Sensor": loadDetection()}
			db.child(parent).child(subsystem).update(data)
			sleep(60)
	except (KeyboardInterrupt, SystemExit):
		print("Exiting bedDetection.py")
		GPIO.cleanup()
		shutil.rmtree("images")

if __name__ == "__main__":
	main()
