#frontend.py implements the client side website GUI using dash and plotly. 

import backend
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State

#Initialize dash application
app = dash.Dash(__name__)

#Define each HTML component
interval = dcc.Interval(id = "interval", interval = 5000) # Update every 5 secs
header = html.H1("SprayClock")
dropdown = html.Div(["Alarms", dcc.Dropdown(
	id = "dropdown_alarms",
	options = backend.get_alarms(), #grab alarms from backend.py

	searchable = False,
	clearable = False,
	style = {'width': '45%'},
	placeholder = "Current Alarms")])
dropdown1 = dcc.Dropdown(
	id = "dropdown_days",
	options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],

	searchable = False,
	style = {'width': '50%'},
	placeholder = "Select a day of the week")
input = dcc.Input(
	id = "alarm_input",
	type = "text",
	maxLength = 5,
	placeholder = "Ex: 08:00",
	debounce = True)
addBtn = html.Button("Set Alarm", id = "setButton", title = "Adds alarm", n_clicks = 0)
removeBtn = html.Button("Remove Alarm", id = "removeButton", title = "Removes current alarm selected in dropdown", n_clicks = 0)
userinteractions = html.Div(id = "userinteractions", children="Waiting for user input")
subheader = html.H3("Sleep Data")
graph = dcc.Graph(
	id = "sleep_data",
	figure = backend.make_graph())
dropdown2 = dcc.Dropdown(
	id = "dropdown_graph",
	options = ["Past Week", "Past Month"],
	value = "Past Month",
	style = {'width': '40%'},
	searchable = False,
	clearable = False)

#Define HTML layout
body = [header, html.Hr(), dropdown, input, dropdown1, addBtn, removeBtn, userinteractions, html.Hr(), subheader, graph, dropdown2]
app.layout = html.Div(children = body)

#Update alarms in dropdown and firebase depending on button click
@app.callback(
	Output("dropdown_alarms", "options"),
	Output("userinteractions", "children"),
	Input("setButton", "n_clicks"),
	Input("removeButton", "n_clicks"),
	Input("dropdown_alarms", "value"),
	Input("dropdown_days", "value"),
	State("alarm_input", "value"))
def update_alarms(addBtn, removeBtn, selected_alarm, day_input, time_input):
	btn_click = [p['prop_id'] for p in callback_context.triggered][0] #Get most recent button click
	if "setButton" in btn_click:
		if (day_input == None) and (time_input == None):
			text = 'Invalid time input and no day has been selected from dropdown!'
		elif (day_input != None) and (time_input == None or len(time_input) != 5):
			text = 'Time input needs to be in 24:00 format! Ex. 08:30'
		elif (day_input == None) and (time_input != None and len(time_input) == 5):
			text = 'No day has been selected in dropdown!'
		elif (day_input != None) and (time_input != None and len(time_input) == 5):
			backend.setButtonClicked(day_input, time_input)
			text = 'Alarm has been set!'
	elif "removeButton" in btn_click:
		if (selected_alarm != None):
			backend.removeButtonClicked(selected_alarm)
			text = 'Alarm has been removed!'
		else:
			text = 'No alarm has been selected in dropdown!'
	else:
		text = 'Waiting for user input'
	return [{'label': alarm, 'value': alarm} for alarm in backend.get_alarms()], text

#Update graph depending on value selected in dropdown
@app.callback(
	Output("sleep_data", "figure"),
	Input("dropdown_graph", "value"))
def update_graph(time_length):
	return backend.make_graph(time_length)

#Start website/dash application
if __name__ == "__main__":
	app.run_server(debug = True, host = "0.0.0.0", port = "8050")
