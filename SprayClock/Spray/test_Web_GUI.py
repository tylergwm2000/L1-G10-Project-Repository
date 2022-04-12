import frontend
import backend
import pyrebase
from datetime import datetime
import pytest

#Firebase config
config = {
	"apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
	"authDomain": "sprayclock-4e902.firebaseapp.com",
	"databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
	"storageBucket": "sprayclock-4e902.appspot.com"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

#Testing Set Alarm button press
def test_SettingAlarmCommunication():
	backend.setButtonClicked("Monday", "14:50") # Set with Monday and 14:50 input
	alarms = backend.getAlarms()
	expected = "Monday 14:50"
	assert alarms[len(alarms)-1] == expected # Check last alarm is the newly set alarm
	data = db.child("Subsystem Status").child("Web GUI").get()
	expected = {"alarmTime": "14:50", "deleteAlarm": False, "setAlarm": True}
	assert data.val() == expected # Check Web GUI status is updated

#Testing Delete Alarm button press
def test_DeleteAlarmCommunication():
	backend.removeButtonClicked("Monday 14:50") # Delete previously set Monday 14:50 alarm
	alarms = backend.getAlarms()
	for alarm in alarms:
		assert alarm != "Monday 14:50" # Check that alarm isn't in the list of alarms
	data = db.child("Subsystem Status").child("Web GUI").get()
	expected = {"alarmTime": "14:50", "deleteAlarm": True, "setAlarm": False}
	assert data.val() == expected # Check Web GUI status is updated

#Testing getting alarms from Firebase
def test_GetAlarmsCommunication():
	options = backend.getAlarms()
	data = db.child("Set Alarms").get()
	data_list = data.each()
	expected = []
	for data in data_list:
		expected.append(data.val()["Day"] + ' ' + data.val()["Time"])
	assert expected == options # Check get alarms method gets all the alarms


