import pyrebase
from time import sleep
from datetime import datetime
import time
import RPi.GPIO as GPIO

def init_firebase():
	config = {
		"apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
		"authDomain": "sprayclock-4e902.firebaseapp.com",
		"databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
		"storageBucket": "sprayclock-4e902.appspot.com"}
	firebase = pyrebase.initialize_app(config)
	db = firebase.database()
	return db


def get_alarms():
	db = init_firebase()
	allData = db.child("Set Alarms").get()
	allData_list = allData.each()
	options = []
	for data in allData_list:
		alarmtime = datetime.strptime(data.val()["Time"], "%H:%M")
		options.append(alarmtime)
	return options

def showTime():
	while True:
		time.sleep(2)
		time_now = datetime.now() #time_now is the current ti
		curr_time = time_now.strftime("%H:%M") #curr_time is what will be used to print current time
		curr_date = time.now.strftime("%d/%m/%Y") #curr_date is what will be used to print current date
		print("Current date is:",curr_date)
		print(curr_time)
		break

def ringAlarm():
	new_alarm = get_alarms()
	time_now = datetime.now()
	for alarm in new_alarm:
		if new_alarm == time_now.strftime("%H:%M"):
			print("alarmClockRinging")
			deleteAlarm(new_alarm)
			return True
		else:
			print("alarmClockIdle")
			return False

def deleteAlarm(alar): #alar is a the alarm which had just rang
	key = 0
	alarms = get_alarms() #alarms is a list of alarms
	for alarm in alarms: #checking every alarm object in alarms
		if alarm != alar: #check when the alarm object is alar
			key += 1
	db.child("Set Alarms").child(key).remove() 

def buttonPressed(channel):
	print("Button was pushed!")
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(14,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up

def main():
	db = init_firebase()
	parent = "Subsystem Status"
	subsystem = "Alarm Clock"
	data = {"Buzzer": ringAlarm(), "Button": False}
	db.child(parent).child(subsystem).update(data)

if __name__ == "__main__":
	main()
