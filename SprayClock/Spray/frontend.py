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
	value = "",
	searchable = False,
	clearable = False,
	style = {'width': '30%'},
	placeholder = "Current Alarms")])
dropdown1 = dcc.Dropdown(
	id = "dropdown_days",
	options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
	value = "",
	searchable = False,
	style = {'width': '40%'},
	placeholder = "Select a day of the week")
input = dcc.Input(
	id = "alarm_input",
	type = "text",
	maxLength = 5,
	placeholder = "Ex: 08:00",
	debounce = True)
addBtn = html.Button("Set Alarm", id = "setButton", title = "Adds alarm", n_clicks = 0)
removeBtn = html.Button("Remove Alarm", id = "removeButton", title = "Removes current alarm selected in dropdown", n_clicks = 0)
subheader = html.H3("Sleep Data")
graph = dcc.Graph(
	id = "sleep_data",
	figure = backend.make_graph())
dropdown2 = dcc.Dropdown(
	id = "dropdown_graph",
	options = ["Week", "Month"],
	value = "Month",
	style = {'width': '25%'},
	searchable = False,
	clearable = False)

#Define HTML layout
body = [interval, header, html.Hr(), dropdown, input, dropdown1, addBtn, removeBtn, html.Hr(), subheader, graph, dropdown2]
app.layout = html.Div(children = body)

#Update alarms in dropdown and firebase depending on button click
@app.callback(
	Output("dropdown_alarms", "options"),
	Input("setButton", "n_clicks"),
	Input("removeButton", "n_clicks"),
	Input("dropdown_alarms", "value"),
	Input("dropdown_days", "value"),
	State("alarm_input", "value"))
def update_alarms(addBtn, removeBtn, selected_alarm, day_input, time_input):
	btn_click = [p['prop_id'] for p in callback_context.triggered][0] #Get most recent button click
	if "setButton" in btn_click:
		print("Hello")
		backend.setButtonClicked(day_input, time_input)
	elif "removeButton" in btn_click:
		print("Goodbye")
		backend.removeButtonClicked(selected_alarm)
	return [{'label': alarm, 'value': alarm} for alarm in backend.get_alarms()]

#Start website/dash application
if __name__ == "__main__":
	app.run_server(debug = True, host = "0.0.0.0", port = "8050")
