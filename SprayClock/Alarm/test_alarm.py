import main
import pytest

db = main.init_firebase()

#testing the get_alarms() function

def test_get_alarms():
	allAlarms=db.child("Set Alarms").get()
	allData_list = allData.each()
	options = []
	for data in allData_list:
                alarmtime = datetime.strptime(data.val()["Time"], "%H:%M")
                options.append(alarmtime)
	assert options==main.get_alarms()

def test_showTime():
	current_exp_time=main.showTime()
   time_now = datetime.now()
         curr_time = time_now.strftime("%H:%M")
	assert curr_time = current_exp_time

def test_ringAlarm():
	time_now = datetime.now()
	curre_time = time_now.strftime("%H:%M")
	new_alarm = {"Day" : "Monday", "Time": curre_time}
	db.child("Set Alarms").child(5).set(new_alarm)
	expected = main.ringAlarm()
	assert True == expected

def test_buttonPressed():
	print("button was recognized")
	expected ==main.buttonPressed()
	assert True == expected 

