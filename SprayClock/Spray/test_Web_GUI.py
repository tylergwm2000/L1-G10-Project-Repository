import frontend
import backend
import pyrebase
from datetime import datetime
import pytest

config = {
	"apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
	"authDomain": "sprayclock-4e902.firebaseapp.com",
	"databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
	"storageBucket": "sprayclock-4e902.appspot.com"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def test_SettingAlarmCommunication():
	backend.setButtonClicked("Monday", "14:50")
	alarms = backend.getAlarms()
	expected = "Monday 14:50"
	assert alarms[len(alarms)-1] == expected
	data = db.child("Subsystem Status").child("Web GUI").get()
	expected = {"alarmTime": "14:50", "deleteAlarm": False, "setAlarm": True}
	assert data.val() == expected

def test_DeleteAlarmCommunication():
	backend.removeButtonClicked("Monday 14:50")
	alarms = backend.getAlarms()
	for alarm in alarms:
		assert alarm != "Monday 14:50"
	data = db.child("Subsystem Status").child("Web GUI").get()
	expected = {"alarmTime": "14:50", "deleteAlarm": True, "setAlarm": False}
	assert data.val() == expected

def test_GetAlarmsCommunication():
	options = backend.getAlarms()
	data = db.child("Set Alarms").get()
	data_list = data.each()
	expected = []
	for data in data_list:
		expected.append(data.val()["Day"] + ' ' + data.val()["Time"])
	assert expected == options


