#backend.py implements all the functions needed by frontend.py to run a client-side website.

import pyrebase
from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px

#Initialize firebase database
config = {
	"apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
	"authDomain": "sprayclock-4e902.firebaseapp.com",
	"databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
	"storageBucket": "sprayclock-4e902.appspot.com"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

#Get alarms from Firebase
def get_alarms():
	allAlarms = db.child("Set Alarms").get()
	allAlarms_list = allAlarms.each()
	options = []
	for alarm in allAlarms_list:
		alarmTime = datetime.strptime(alarm.val()["Time"], "%H:%M").time()
		dayOfAlarm = alarm.val()["Day"]
		options.append(dayOfAlarm + " " + str(alarmTime))
	return options

#Make sleep data graph using plotly.express
def make_graph():
	allSleepData = db.child("Sleep Data").get()
	allData_list = allSleepData.each()
	x = []
	y = []
	for data in allData_list:
		x.append(data.key())
		waketime = datetime.strptime(data.val()["WakeTime"], "%H:%M").time()
		sleeptime = datetime.strptime(data.val()["SleepTime"], "%H:%M").time()
		wake = datetime.combine(date.today(), waketime)
		if (sleeptime.hour > 12): #if time slept was before 24:00
			sleep = datetime.combine(date.today() - timedelta(days=1), sleeptime)
		else: #person slept after 24:00
			sleep = datetime.combine(date.today(), sleeptime)
		timeslept = wake - sleep
		hours_slept = timeslept/timedelta(hours=1) #Change to hours only format from deltatime format
		y.append(hours_slept)
	names = ["Date", "Hours Slept"]
	result = []
	for a in zip(x, y):
		result.append(a)
	df = pd.DataFrame(result, columns=names)
	fig = px.bar(df, x="Date", y="Hours Slept")
	return fig

#Set button clicked
def setButtonClicked(day, time):
	alarms = get_alarms()
	key = 0
	for alarm in alarms:
		key += 1
	time = datetime.strptime(time, "%H:%M").time()
	data = {"Day": day, "Time": str(time)}
	db.child("Set Alarms").child(key).set(data)
	data = {"alarmTime": time, "setAlarm": True, "deleteAlarm": False}
	db.child("Subsystem Status").child("Web GUI").update(data)

#Remove button clicked
def removeButtonClicked(dayTime):
	alarms = get_alarms()
	alarmExists = False
	key = 0
	for alarm in alarms:
		if dayTime == alarm:
			print("Alarm Found")
			alarmExists = True
			break
		else:
			key += 1
	if alarmExists:
		db.child("Set Alarms").child(key).remove()
		
	time = datetime.strptime(dayTime)
	data = {"alarmTime": time, "setAlarm": False, "deleteAlarm": True}
	db.child("Subsystem Status").child("Web GUI").update(data)
