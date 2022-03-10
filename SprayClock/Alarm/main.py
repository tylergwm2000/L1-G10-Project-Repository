import pyrebase
from time import sleep
import datetime
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
	    time_now = datetime.datetime.now() #time_now is the current time
 	    curr_time = time_now.strftime("%H:%M") #curr_time is what will be used to print current time
	    curr_date = time.now.strftime("%d/%m/%Y") #curr_date is what will be used to print current date
	    print("Current date is:",curr_date)
	    print(curr_time)
	    break

def ringAlarm():
	new_alarm = get_alarms()
	for alarm in new_alarm:
		if new_alarm == time_now.strftime("%H:%M"):
			print("alarmClockRinging")
			return True
		else:
	   	     	print("alarmClockIdle")
			return False

#def deleteAlarm():
#	if ringAlarm(new_alarm)==True

def main():
	db = init_firebase()
	parent = "Subsystem Status"
	subsystem = "Alarm Clock"
	data = {"Buzzer": ringAlarm(), "Button": False}
	db.child(parent).child(subsystem).update(data)
if __name__ == "__main__":
	main()
