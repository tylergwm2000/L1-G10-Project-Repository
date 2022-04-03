import pyrebase
from time import sleep
from datetime import datetime
import time
import RPi.GPIO as GPIO

#As this file does not exceed 70 lines, it does not meet the requirement of 100 lines, therefore I will b uploading a second file to EduFLow
#This program was created to design a simple alarm clock for use in our team project the SprayClock.
#It contains functions to get any set alarms from a list, a function to show the current time and date, a function which will ring once the current time matches time of alam, a function for push button
#and finally a main method to act as our driver code to send information to the firebase which is configured in our fake function init_firebase()
#Note that the firebase configuration was made into a function so that it will not have to be configured each time in seperate files

#The logic used for the GPIO below was created after using the following link for reference https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
#Need to add display and buzzer GPIO setup
GPIO.setwarnings(False) # No warning will be recognized at the time
GPIO.setmode(GPIO.BCM) # This will be used to let us use pin numbers
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 8 to be an input pin
GPIO.add_event_detect(14,GPIO.RISING,callback=buttonPressed) # Adding an event from pin 14
#Is this necessary? statement = input("If you want to quit, press enter\n") # Program will run until someone has clicked enter

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
                alarmtime = data.val()["Time"]
		dayOfAlarm = data.val()["Day"]
                options.append(dayOfAlarm + " " + alarmTime)
        return options

def showTime():
        now = datetime.now() #now is the current datetime
	curr_time = now.strftime("%H:%M") #curr_time is the current time
	curr_date = now.strftime("%m-%d-%Y") #curr_date is the current date
	#Temporarily prints (Should be displayed on 16x2 Screen)
	print("Current date is: {}".format(curr_date))
	print("Current time is: {}".format(curr_time))

def ringAlarm(alarmStatus = False):
	db = init_firebase()
	camera_detection = db.child("Subsystem Status").child("Bed Detection").child("Camera").get().val()
	load_detection = db.child("Subsystem Status").child("Bed Detection").child("Load Sensor").get().val()
	if (alarmStatus): #If alarm currently ringing, continue
		return True
	if (camera_detection and load_detection): #If user is in bed
        	new_alarm = get_alarms()
        	now = datetime.now()
		weekday = now.weekday()
		curr_time = now.strftime("%H:%M")
        	for alarm in new_alarm:
			alarm_text = alarm.split()
			alarm_day = alarm_text[0].strftime("%A").weekday()
			alarm_time = alarm_text[1].strftime("%H:%M")
                	if alarm_day == weekday and curr_time == alarm_time: #If it is currently the alarmtime and day of alarm
                        	print("alarmClockRinging")
				#Need to implement buzzer ringing here
                        	return True
	else:
		print("alarmClockIdle")
		return False

def buttonPressed(channel):
        print("Buttonpressed")
	db = init_firebase()
	#Update Subsystem Status table
	data = {"Button": True, "Buzzer": False}
	#Only update tables if Alarm is ringing
	if (db.child("Subsystem Status").child("Alarm Clock").child("Buzzer").get().val() == True):
		db.child("Subsystem Status").child("Alarm Clock").update(data)
		#Update Sleep Data table
		now = datetime.now()
		curr_time = now.strftime("%H:%M")
		sleep_day = (now - timedelta(days = 1)).strftime("%m-%d-%Y")
		data = {"WakeTime": curr_time}
		db.child("Sleep Data").child(sleep_day).update(data)

def main():
	try:
        	db = init_firebase()
        	parent = "Subsystem Status"
        	subsystem = "Alarm Clock"
		while(True):
			showTime()
			alarmStatus = ringAlarm(alarmStatus) #Check if alarm should ring or not
        		data = {"Buzzer": alarmStatus}
        		db.child(parent).child(subsystem).update(data)
			alarmStatus = db.child(parent).child(subsystem).child("Buzzer").get().val() #If button ever pressed update alarmStatus to False
			sleep(60)
	except(KeyboardInterrupt, SystemExit):
		print("Alarm Subsystem Exiting")
		GPIO.cleanup()

if __name__ == "__main__":
        main()

