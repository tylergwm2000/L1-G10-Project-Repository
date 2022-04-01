# backend.py implements all the functions needed by frontend.py to run a client-side
# website. It performs all the communication necessary with the Firebase and creates
# a data graph using plotly.
import pyrebase
from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px

# Initialize firebase database
config = {
	"apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
	"authDomain": "sprayclock-4e902.firebaseapp.com",
	"databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
	"storageBucket": "sprayclock-4e902.appspot.com"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


# Get alarms from Firebase and returns a list to be used for dropdown
# of alarms in frontend.py
# Output: list of alarms
def getAlarms():
	# Get alarms from Firebase and put in a list
	allAlarms = db.child("Set Alarms").get()
	allAlarmsList = allAlarms.each()
	options = []
	# Iterate through list of alarms and arrange alarm data into one list
	for alarm in allAlarmsList:
		alarmTime = alarm.val()["Time"]
		dayOfAlarm = alarm.val()["Day"]
		options.append(dayOfAlarm + " " + alarmTime)
	return options


# Make sleep data graph using plotly.express
# Input: Value of timelength selected in dropdown below graph in Web GUI (Past Month or Past Week)
# Output: bar graph figure of sleep data
def makeGraph(timelength="Past Month"):
	# Get sleep data from Firebase and put into list
	allSleepData = db.child("Sleep Data").get()
	allDataList = allSleepData.each()
	# If statements for dropdown below graph for time length of graph data
	if timelength == "Past Month":
		allDataList = allDataList[-30:] # 30 latest data points
	elif timelength == "Past Week":
		allDataList = allDataList[-7:] # 7 latest data points
	# Empty lists for storing data to create graph
	x = []
	y = []
	# Iterate through sleep data list, record date and calculate and record amount
	# of sleep into x and y list respectively
	for data in allDataList:
		x.append(data.key()) # Key is date to be added to x list
		#if (data.val()["WakeTime"]): NEED TO IMPLEMENT WHEN NO WAKETIME CHILD
		#	break
		# Convert from string to datetime.time type
		waketime = datetime.strptime(data.val()["WakeTime"], "%H:%M").time()
		sleeptime = datetime.strptime(data.val()["SleepTime"], "%H:%M").time()
		# Combine datetime.time with day for a datetime type
		wake = datetime.combine(date.today(), waketime)
		if (sleeptime.hour > 12): # if time slept was before 24:00 (last night)
			sleep = datetime.combine(date.today() - timedelta(days=1), sleeptime)
		else: # person slept after 24:00 (this morning)
			sleep = datetime.combine(date.today(), sleeptime)
		# Calculate amount of sleep and change to hours only format then add to y list
		timeslept = wake - sleep
		hoursSlept = timeslept / timedelta(hours=1)
		y.append(hoursSlept)
	# Create bar graph using x and y lists through plotly
	names = ["Date", "Hours Slept"]
	result = []
	for a in zip(x, y):
		result.append(a)
	df = pd.DataFrame(result, columns=names)
	fig = px.bar(df, x="Date", y="Hours Slept")
	return fig


# Set button clicked in Web GUI, search through all current alarms for user input data, day & time
# If alarm is found then don't add it to the list of alarms
# If alarm is not found then add it to the list and update status of Web GUI
# Input: day selected in dropdown and time entered by user
def setButtonClicked(day, time):
	alarms = getAlarms() # Get list of alarms
	alarmExists = False # Boolean for checking if alarm is in list
	key = len(alarms) # Key for uploading alarm to Firebase
	dayTime = day + " " + time #dayTime string for comparing with list
	# Iterate through list of alarms and check if alarm is in list
	for alarm in alarms:
		if dayTime == alarm:
			alarmExists = True
			break
	# Upload alarm if alarm not in list
	if (not alarmExists):
		data = {"Day": day, "Time": time}
		db.child("Set Alarms").child(key).set(data)
		# Update status of Web GUI
		data = {"alarmTime": time, "setAlarm": True, "deleteAlarm": False}
		db.child("Subsystem Status").child("Web GUI").update(data)


# Remove button clicked in Web GUI, search through all current alarms for selected alarm, dayTime
# If alarm is found then delete it by shifting all alarms after it and removing last alarm in the list
# If alarm successfully deleted, also update status of Web GUI
# Input: Alarm selected in dropdown list of alarms in Web GUI
def removeButtonClicked(dayTime):
	alarms = getAlarms() # Get list of alarms
	alarmExists = False # Boolean for checking if alarm is in list
	key = 0 # Key value of alarm to delete
	# Iterate through list of alarms and check if alarm is in list
	for alarm in alarms:
		if dayTime == alarm:
			alarmExists = True
			break
		else:
			key += 1
	# If alarm was found, shift every alarm after by 1 to delete it
	if alarmExists:
		for i in range((key+1), len(alarms)):
			alarm = db.child("Set Alarms").child(i).get()
			db.child("Set Alarms").child((i-1)).set(alarm.val())
		# Delete last unmoved alarm at end of list
		db.child("Set Alarms").child((len(alarms)-1)).remove()
	# Update status of Web GUI
	stringList = dayTime.split()
	time = stringList[1]
	data = {"alarmTime": time, "setAlarm": False, "deleteAlarm": True}
	db.child("Subsystem Status").child("Web GUI").update(data)
