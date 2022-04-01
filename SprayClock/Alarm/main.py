import pyrebase
from time import sleep
from datetime import datetime
import time
import RPi.GPIO as GPIO

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
                alarmtime = alarm.val()["Time"]
		dayOfAlarm = alarm.val()["Day"]
                options.append(dayOfAlarm + " " + alarmTime)
        return options

def showTime():
        now = datetime.now() #now is the current datetime
	curr_time = now.strftime("%H:%M") #curr_time is the current time
	curr_date = now.strftime("%m-%d-%Y") #curr_date is the current date
	#Temporarily prints (Should be displayed on 16x2 Screen)
	print("Current date is: {}".format(curr_date))
	print(curr_time)

def ringAlarm(alarmStatus = False):
	if (alarmStatus): #If alarm currently ringing, continue
		return True
        new_alarm = get_alarms()
        now = datetime.now()
	weekday = now.weekday()
	curr_time = now.strftime("%H:%M")
        for alarm in new_alarm:
		alarm_text = alarm.split()
		alarm_day = alarm_text[0].strftime("%A").weekday()
		alarm_time = alarm_text[1].strftime("%H:%M")
                if alarm_day == weekday and curr_time == alarm_time:
                        print("alarmClockRinging")
			#Need to implement buzzer ringing here
                        return True
                else:
                        print("alarmClockIdle")
                        return False

def buttonPressed(channel):
        print("Buttonpressed")
	#Update Subsystem Status table
	data = {"Button": True}
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
			alarmStatus = ringAlarm(alarmStatus) #Need to figure out how to turn off alarm once it begins ringing (global variable?)
        		data = {"Buzzer": alarmStatus}
        		db.child(parent).child(subsystem).update(data)
			sleep(60)
	except(KeyboardInterrupt, SystemExit):
		print("Alarm Subsystem Exiting")
		GPIO.cleanup()

if __name__ == "__main__":
        main()

