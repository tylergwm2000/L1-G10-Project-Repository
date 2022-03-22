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

def buttonPressed(channel):
        print("Buttonpressed")
GPIO.setwarnings(False) # No warning will be recognized at the time
GPIO.setmode(GPIO.BCM) # This will be used to let us use pin numbers
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 8 to be an input pin
GPIO.add_event_detect(14,GPIO.RISING,callback=buttonPressed) # Adding an event from pin 14
statement = input("If you want to quit, press enter\n\n") # Program will run until someone has clicked enter
GPIO.cleanup()



def main():
        db = init_firebase()
        parent = "Subsystem Status"
        subsystem = "Alarm Clock"
        data = {"Buzzer": ringAlarm(), "Button": True}
        db.child(parent).child(subsystem).update(data)

if __name__ == "__main__":
        main()

