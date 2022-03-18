#bedDetection.py implements Bed Detection Subsystem and uses the Load Cell and RPi camera
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
def init_firebase():
	config = {
		"apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
		"authDomain": "sprayclock-4e902.firebaseapp.com",
		"databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
		"storageBucket": "sprayclock-4e902.appspot.com"}
	firebase = pyrebase.initialize_app(config)
	db = firebase.database()
	return db

#Perform detection using load sensor by comparing weight of bed with current weight
def loadDetection(hx, bedWeight):
	current = hx.get_grams()
	difference = int(current) - int(bedWeight)
	print(difference)
	if difference > 0:
		return True
	else:
		return False

#Perrform necessary setup than infinitely perform bed detection algorithm and update results to firebase
def main():
	try:
		#Setup firebase, camera, load sensor
		db = init_firebase()
		camera = Camera.init_camera()
		hx = HX711(5,6)
		#Calibrate load sensor
		#checkReady = input("Remove any items from the load sensor. Press any key when ready.")
		#offset = hx.read_average()
		#hx.set_offset(offset)
		#checkReady = input("Place any known weight item on the load sensor. Press any key when ready.")
		#measured_weight = (hx.read_average()-hx.get_offset())
		#item_weight = input("Please enter item's weight in grams.\n>")
		#scale = int(measured_weight)/int(item_weight)
		#hx.set_scale(scale)
		#checkReady = input("Load sensor ready for use, place under bed. Press any key when ready.")
		#Delete images folder if it already exists than create it for storing images
		if os.path.isdir("images"):
			shutil.rmtree("images")
		os.mkdir("images")
		parent = "Subsystem Status"
		subsystem = "Bed Detection"
		key = 0 #Key for naming pictures
		bedWeight = hx.get_grams() #Get weight of the bed
		while (True): #Infinite loop
			now = datetime.now()
			current_time = now.strftime("%H:%M")
			#File locations of where to store image, where tensorflow model is stored, where label for tensorflow model is stored
			imagefile = "images/{}-{}-{}_{}.jpg".format(now.year, now.month, now.day, key)
			modelfile = "Google_MSCOCO_Model/detect.tflite"
			labelfile = "Google_MSCOCO_Model/labelmap.txt"
			#Take image and use for tensorflow object detection API
			Camera.take_image(camera, imagefile)
			cameraDetects = Camera.camera_detection(imagefile, modelfile, labelfile)
			#Check for person detection using load sensor
			loadSensorDetects = loadDetection(hx, bedWeight)
			data = {"Camera": cameraDetects, "Load Sensor": loadSensorDetects}
			#Update results to firebase
			db.child(parent).child(subsystem).update(data)
			if (cameraDetects or loadSensorDetects): #If person has been detected upload current time for time person slept
				data = {"SleepTime": current_time}
				if (now.hour < 24):
					current_day = now.strftime("%m-%d-%Y")
				else:
					current_day = (now - timedelta(days=1)).strftime("%m-%d-%Y")
				db.child("Sleep Data").child(current_day).update(data)
			if (now.hour == 23 and now.minute == 59): #If day is about to change, update key value for image naming 
				key = 0
			else:
				key += 1
			sleep(60) #Iterate through loop every minute
	except (KeyboardInterrupt, SystemExit): #Handling interrupt and system exit
		print("Exiting bedDetection.py")
		GPIO.cleanup()
		shutil.rmtree("images")

if __name__ == "__main__":
	main()
