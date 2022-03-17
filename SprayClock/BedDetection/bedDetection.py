#bedDetection.py implements Bed Detection Subsystem and uses the Load Cell and RPi camera
#Import required libraries
from camera import Camera
import pyrebase
from hx711 import HX711
import RPi.GPIO as GPIO
from time import sleep
import os
import shutil
import datetime

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

def loadDetection(hx, bedWeight):
	#current = hx.get_grams()
	#difference = int(current) - int(bedWeight)
	#if difference > 0:
	#	print(difference)
	#	return True
	#else:
	#	return False
	return True

def main():
	try:
		db = init_firebase()
		camera = Camera.init_camera()
		hx = HX711(5,6)
		#checkReady = input("Remove any items from the load sensor. Press any key when ready.")
		#offset = hx.read_average()
		#hx.set_offset(offset)
		#checkReady = input("Place any known weight item on the load sensor. Press any key when ready.")
		#measured_weight = (hx.read_average()-hx.get_offset())
		#item_weight = input("Please enter item's weight in grams.\n>")
		#scale = int(measaured_weight)/int(item_weight)
		#hx.set_scale(scale)
		#checkReady = input("Load sensor ready for use, place under bed. Press any key when ready.")
		if os.path.isdir("images"):
			shutil.rmtree("images")
		os.mkdir("images")
		parent = "Subsystem Status"
		subsystem = "Bed Detection"
		key = 0
		bedWeight = 5 #hx.get_grams()
		while (True):
			now = datetime.datetime.now()
			imagefile = "images/{}-{}-{}_{}.jpg".format(now.year, now.month, now.day, key)
			modelfile = "Google_MSCOCO_Model/detect.tflite"
			labelfile = "Google_MSCOCO_Model/labelmap.txt"
			Camera.take_image(camera, imagefile)
			data = {"Camera": Camera.camera_detection(imagefile, modelfile, labelfile), "Load Sensor": loadDetection(hx, bedWeight)}
			db.child(parent).child(subsystem).update(data)
			if (now.hour == 23 and now.minute == 59):
				key = 0
			else:
				key += 1
			sleep(60)
	except (KeyboardInterrupt, SystemExit):
		print("Exiting bedDetection.py")
		GPIO.cleanup()
		shutil.rmtree("images")

if __name__ == "__main__":
	main()
