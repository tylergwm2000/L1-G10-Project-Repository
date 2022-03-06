#import required libraries
import pyrebase
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
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

#Initialize dash application
app = dash.Dash(__name__)

#Get alarms from Firebase
def get_alarms():
	allData = db.child("Set Alarms").get()
	print(allData.val())
	allData_list = allData.each()
	options = []
	for data in allData_list:
		alarmtime = datetime.strptime(data.val()["Time"], "%H:%M").time()
		options.append(alarmtime)
	return options

#Make sleep data graph using plotly.express
def make_graph():
	allData = db.child("Sleep Data").get()
	allData_list = allData.each()
	x = []
	y = []
	for data in allData_list:
		x.append(data.key())
		waketime = datetime.strptime(data.val()["WakeTime"], "%H:%M").time()
		sleeptime = datetime.strptime(data.val()["SleepTime"], "%H:%M").time()
		wake = datetime.combine(date.today(), waketime)
		if (sleeptime.hour > 12): #if time slept was before 24:00
			sleep = datetime.combine(date.today() - timedelta(days=1), sleeptime)
		else:
			sleep = datetime.combine(date.today(), sleeptime)
		timeslept = wake - sleep
		hours_slept = timeslept/timedelta(hours=1) #change to hours only format from deltatime format
		y.append(hours_slept)
	names = ["Date", "Hours Slept"]
	result = []
	for a in zip(x, y):
		result.append(a)
	df = pd.DataFrame(result, columns=names)
	fig = px.bar(df, x="Date", y="Hours Slept")
	return fig

#Define HTML layout
interval = dcc.Interval(id = "interval", interval = 5000) #update every 5 secs
header = html.H1("SprayClock")
dropdown = html.Div(["Alarms", dcc.Dropdown(
	id = "dropdown_alarms",
	options = ["08:00"], #grab alarms from database
	value = "",
	searchable = False,
	clearable = False,
	placeholder = "Current Alarms")])
input = html.Div(["Input time in %H:%M format", dcc.Input(
	id = "alarm_input",
	type = "text",
	maxLength = 5,
	placeholder = "08:00",
	debounce = True)])
addBtn = html.Button("Add Alarm", id = "addButton", title = "Adds alarm input in textbox", n_clicks = 0)
removeBtn = html.Button("Remove Alarm", id = "removeButton", title = "Removes current alarm selected in dropdown", n_clicks = 0)
subheader = html.H3("Sleep Data")
graph = dcc.Graph(
	id = "sleep_data",
	figure = make_graph())
body = [interval, header, dropdown, input, addBtn, removeBtn, subheader, graph]
app.layout = html.Div(children = body)

#Update dropdown & firebase on button click
@app.callback(Output("dropdown_alarms", "options"), Input("addButton", "n_clicks"), Input("removeButton", "n_clicks"), Input("alarm_input", "value"))
def update_dropdown(addBtn, removeBtn, input):
	btn_click = [p['prop_id'] for p in callback_context.triggered][0]
	if "addButton" in btn_click:
		print("Hello")
	elif "removeButton" in btn_click:
		print("Goodbye")

#Start website/dash application
if __name__ == "__main__":
	app.run_server(debug=True, host="0.0.0.0", port="8050")
