#bedDetection.py implements Bed Detection Subsystem and uses the Load Cell and RPi camera through the
#hx711 and camera python files. This program will use the load cell to measure weight values and compare
#them to determine if a person is in bed or not. The RPi camera will be used to take images which can be
#sent through a tensorflow model to determine if a person is detected in the image or not.

#Import required libraries
from camera import Camera
import pyrebase
from hx711 import HX711
import RPi.GPIO as GPIO
from time import sleep
import os
import shutil
from datetime import datetime, timedelta

#Initialize firebase database and return as object
def initFirebase():
	config = {
		"apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
		"authDomain": "sprayclock-4e902.firebaseapp.com",
		"databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
		"storageBucket": "sprayclock-4e902.appspot.com"}
	firebase = pyrebase.initialize_app(config)
	db = firebase.database()
	return db

#Perform calibration of load sensor by using known weight item
#Input: load sensor class hx711 object
def calibrateLoadSensor(hx):
	print("Calibrating Load Sensor: ")
	checkReady = input("Please remove any item from the load sensor. Press any key when ready.")
	offset = hx.read_average()
	print("Offset set to {}".format(offset))
	hx.set_offset(offset)
	checkReady = input("Place any known weight item on the load sensor. Press any key when ready.")
	measuredWeight = (hx.read_average() - hx.get_offset())
	itemWeight = input("Please enter item's weight in grams. \n>")
	scale = int(measuredWeight)/int(itemWeight)
	print("The ratio from analog value to grams is {}".format(scale))
	hx.set_scale(scale)
	checkReady = input("Load sensor is now calibrated, please place under bed mattress. Press any key when ready.")

#Perform detection using load sensor by comparing weight of bed with current weight
#Input: load sensor class hx711 object and (long) bed weight value
#Output: returns boolean of whether person is detected (True) or not (False)
def loadDetection(hx, bedWeight):
	print("Load Sensor: ")
	print("Bed Weight: {}g".format(bedWeight))
	current = hx.get_grams()
	hx.power_down()
	sleep(0.001)
	hx.power_up()
	print("Current Weight: {}g\n".format(current))
	difference = int(current) - int(bedWeight)
	if difference > 1000: #Difference greater than at least 1kg
		return True
	else:
		return False

#Update results to Firebase
#Input: database object, boolean of whether camera detects person, boolean of whether load sensor detects person,
#       boolean of whether sleep time has been set yet, current datetime object
#Output: returns boolean of whether sleep time has been set
def updateFirebase(db, cameraDetects, loadSensorDetects, sleepTimeSet, now):
	#Update Subsystem Status table
	parent = "Subsystem Status"
	subsystem = "Bed Detection"
	currentTime = now.strftime("%H:%M")
	data = {"Camera": cameraDetects, "Load Sensor": loadSensorDetects}
	db.child(parent).child(subsystem).update(data)
	#Update Sleep Data table
	parent = "Sleep Data"
	if (cameraDetects and loadSensorDetects and (not sleepTimeSet)): #If person has been detected for the first time set current time as time person slept
		data = {"SleepTime": currentTime}
		if (now.hour >= 12 and now.hour <= 23): #Person slept between 12:00 PM and 12:00 AM
			currentDay = now.strftime("%m-%d-%Y")
		else: #Person slept between 12:00 AM and 12:00 PM next day
			currentDay = (now - timedelta(days = 1)).strftime("%m-%d-%Y")
		db.child(parent).child(currentDay).update(data)
		return True
	return sleepTimeSet

#Perform necessary setup than infinitely perform bed detection algorithm and update results to firebase
def main():
	try:
		#Setup firebase, camera, load sensor
		db = initFirebase()
		camera = Camera.init_camera()
		hx = HX711(5,6)
		calibrateLoadSensor(hx)
		#Delete images folder if it already exists then create it for storing temporary images
		if os.path.isdir("images"):
			shutil.rmtree("images")
		os.mkdir("images")
		key = 0 #Key for naming pictures
		#Get weight of the bed then prepare for next reading
		bedWeight = hx.get_grams()
		hx.power_down()
		sleep(0.001)
		hx.power_up()
		sleepTimeSet = False
		while (True): #Infinite loop
			now = datetime.now()
			#File locations of where to store image, where tensorflow model is stored, where label for tensorflow model is stored
			imagefile = "images/{}-{}-{}_{}.jpg".format(now.year, now.month, now.day, key)
			modelfile = "Google_MSCOCO_Model/detect.tflite"
			labelfile = "Google_MSCOCO_Model/labelmap.txt"
			#Take image and use for tensorflow object detection API
			Camera.take_image(camera, imagefile)
			cameraDetects = Camera.camera_detection(imagefile, modelfile, labelfile)
			#Check for person detection using load sensor
			loadSensorDetects = loadDetection(hx, bedWeight)
			#Update Firebase and necessary variables
			sleepTimeSet = updateFirebase(db, cameraDetects, loadSensorDetects, sleepTimeSet, now)
			if (now.hour == 23 and now.minute == 59): #If day is about to change, reset key value for image naming
				key = 0
			else:
				key += 1
			if (db.child("Subsystem Status").child("Alarm Clock").child("Button").get().val()): #If person has woken up, reset sleepTimeSet boolean
				sleepTimeSet = False
			sleep(10) #Iterate through loop every minute
	except (KeyboardInterrupt, SystemExit): #Handling interrupt and system exit
		print("Exiting bedDetection.py")
		GPIO.cleanup()
		shutil.rmtree("images")

if __name__ == "__main__":
	main()
