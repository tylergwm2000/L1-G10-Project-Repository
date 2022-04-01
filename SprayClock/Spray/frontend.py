#frontend.py implements the client side website GUI using dash and plotly.

import backend
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State

#Initialize dash application
app = dash.Dash(__name__)

#Define each HTML component
header = html.H1("SprayClock")
dropdown = html.Div(["Alarms", dcc.Dropdown(
	id = "dropdownAlarms",
	options = backend.getAlarms(), #grab alarms from backend.py
	searchable = False,
	clearable = False,
	style = {'width': '45%'},
	placeholder = "Current Alarms")])
dropdown1 = dcc.Dropdown(
	id = "dropdownDays",
	options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
	searchable = False,
	style = {'width': '50%'},
	placeholder = "Select a day of the week")
input = dcc.Input(
	id = "alarmInput",
	type = "text",
	maxLength = 5,
	placeholder = "Ex: 08:00",
	debounce = True)
addBtn = html.Button("Set Alarm", id = "setButton", title = "Adds alarm of input information", n_clicks = 0)
removeBtn = html.Button("Remove Alarm", id = "removeButton", title = "Removes current alarm selected in dropdown", n_clicks = 0)
userinteractions = html.Div(id = "userinteractions", children="Waiting for user input")
subheader = html.H3("Sleep Data")
graph = dcc.Graph(
	id = "sleepData",
	figure = backend.makeGraph())
dropdown2 = dcc.Dropdown(
	id = "dropdownGraph",
	options = ["Past Week", "Past Month"],
	value = "Past Month",
	style = {'width': '40%'},
	searchable = False,
	clearable = False)

#Define HTML layout
body = [header, html.Hr(), dropdown, input, dropdown1, addBtn, removeBtn, userinteractions, html.Hr(), subheader, graph, dropdown2]
app.layout = html.Div(children = body)

#Update alarms in dropdown and firebase depending on button click
#Input: setButton clicks, removeButton clicks, value selected in alarms dropdown, value selected in days dropdown, value entered in textbox input
#Output: dropdown alarms list, text under buttons describing user interactions
@app.callback(
	Output("dropdownAlarms", "options"),
	Output("userinteractions", "children"),
	Input("setButton", "n_clicks"),
	Input("removeButton", "n_clicks"),
	Input("dropdownAlarms", "value"),
	Input("dropdownDays", "value"),
	State("alarmInput", "value"))
def updateAlarms(addBtn, removeBtn, selectedAlarm, dayInput, timeInput):
	btnClick = [p['prop_id'] for p in callback_context.triggered][0] #Get most recent button click
	if "setButton" in btnClick: #If set button clicked
		if (dayInput == None) and (timeInput == None): #If no inputs
			text = 'Invalid time input and no day has been selected from dropdown!'
		elif (dayInput != None) and (timeInput == None or len(timeInput) != 5): #Incorrect time input
			text = 'Time input needs to be in 24:00 format! Ex. 08:30'
		elif (dayInput == None) and (timeInput != None and len(timeInput) == 5): #Day dropdown has nothing selected
			text = 'No day has been selected in dropdown!'
		elif (dayInput != None) and (timeInput != None and len(timeInput) == 5): #Correct inputs
			backend.setButtonClicked(dayInput, timeInput)
			text = 'Alarm has been set!'
	elif "removeButton" in btnClick: #If remove button clicked
		if (selectedAlarm != None): #Alarm selected in dropdown
			backend.removeButtonClicked(selectedAlarm)
			text = 'Alarm has been removed!'
		else: #No alarm selected in dropdown
			text = 'No alarm has been selected in dropdown!'
	else: #Idle state
		text = 'Waiting for user input'
	return [{'label': alarm, 'value': alarm} for alarm in backend.getAlarms()], text

#Update graph depending on value selected in dropdown
#Input: value selected in timelength dropdown below graph
#Output: updated graph figure
@app.callback(
	Output("sleepData", "figure"),
	Input("dropdownGraph", "value"))
def updateGraph(timeLength):
	return backend.makeGraph(timeLength)

#Start website/dash application
if __name__ == "__main__":
	app.run_server(debug = True, host = "0.0.0.0", port = "8050")
