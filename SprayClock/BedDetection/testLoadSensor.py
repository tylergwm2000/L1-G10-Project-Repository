#testLoadSensor.py performs load sensor setup, calibration then testing of load sensor.

import RPi.GPIO as GPIO
import time
from hx711 import HX711
import sys

#Initialize load sensor
hx = HX711(5, 6)

#Setup load sensor
def setup():
	print("Initializing. Please ensure that scale is empty")
	ready = False
	while not ready:
		if (GPIO.input(hx.DOUT) == 0):
			ready = False
		if (GPIO.input(hx.DOUT) == 1):
			print("Scale is ready!")
			ready = True

#Perform calibration of load sensor
def calibrate():
	readyCheck = input("Empty the scale. Press any key when ready.")
	offset = hx.read_average()
	print("The offset is: {}".format(offset))
	hx.set_offset(offset)
	print("Place an item of known weight on the scale.")
	readyCheck = input("Press any key to continue.")
	measured_weight = (hx.read_average()-hx.get_offset())
	item_weight = input("Please enter the item's weight in grams. \n>")
	scale = int(measured_weight)/int(item_weight)
	hx.set_scale(scale)
	print("The ratio to grams is: {}".format(scale))

#Clean GPIO as exit program
def cleanAndExit():
	print("Cleaning up...")
	GPIO.cleanup()
	print("Bye!")
	sys.exit()

#Main function 
if __name__ == "__main__":
	setup()
	calibrate()
	try:
		userinput = False
		while not userinput:
			val = hx.get_grams()
			hx.power_down()
			time.sleep(0.001)
			hx.power_up()
			print("Item weight is {} grams.\n".format(val))
			choice = input("Please choose:\n [1]Recalibrate \n [2]Display offset and scale and weight an item\n [0]Clean and exit the system")
			if choice == '1':
				calibrate()
			elif choice == '2':
				print("\nOffset: {}\nScale: {}".format(hx.get_offset(), hx.get_scale()))
			elif choice == '0':
				userinput = True
				cleanAndExit()
			else:
				print("Invalid input.\n")
	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()
