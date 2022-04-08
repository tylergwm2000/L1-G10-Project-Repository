import main
import pytest

db = main.init_firebase()

#testing the get_alarms() function

def test_get_alarms():
	allAlarms=db.child("Set Alarms").get()
	allData_list = allData.each()
	options = []
	for data in allData_list:
                alarmtime = data.val()["Time"]
		dayOfAlarm = data.val()["Day"]
                options.append(alarmtime + " " + dayofAlarm)
	assert options==main.get_alarms()

def test_ringAlarm():
	db.child("Subsystem Status").child("Bed Detection").child("Camera").set(True)
	db.child("Subsystem Status").child("Bed Detection").child("Load Sensor").set(True)
	alarms = main.get_alarms()
	time_now = datetime.now()
	curre_time = time_now.strftime("%H:%M")
	weekday = time_now.weekday()
	new_alarm = {"Day" : weekday, "Time": curre_time}
	db.child("Set Alarms").child(len(alarms)).set(new_alarm)
	expected = main.ringAlarm()
	assert True == expected

def test_buttonPressed():
	print("button was recognized")
	expected ==main.buttonPressed()
	assert True == expected 

