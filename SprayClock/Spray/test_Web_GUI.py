import website
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
	website.setButtonClicked("14:50")
	data = db.child("Subsystem Status").child("Web GUI").get()
	expected = {"alarmTime": "14:50", "deleteAlarm": False, "setAlarm": True}
	assert data.val() == expected

def test_DeleteAlarmCommunication():
	website.removeButtonClicked("10:20")
	data = db.child("Subsystem Status").child("Web GUI").get()
	expected = {"alarmTime": "10:20", "deleteAlarm": True, "setAlarm": False}
	assert data.val() == expected

def test_GetAlarmsCommunication():
	options = website.get_alarms()
	data = db.child("Set Alarms").get()
	data_list = data.each()
	expected = []
	for data in data_list:
		expected.append(datetime.strptime(data.val()["Time"], "%H:%M"))
	assert expected == options


