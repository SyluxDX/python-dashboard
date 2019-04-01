""" Part 5 Tutorial dash """
import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader.data import DataReader
from collections import deque
import plotly.graph_objs as go
import random
import time


class VehicleData:
	def __init__(self, max_lenght=50):
		self.times = deque(maxlen=max_lenght)
		self.oil_temp = deque(maxlen=max_lenght)
		self.intake_temp = deque(maxlen=max_lenght)
		self.coolant_temp = deque(maxlen=max_lenght)
		self.rpm = deque(maxlen=max_lenght)
		self.speed = deque(maxlen=max_lenght)
		self.throttle_pos = deque(maxlen=max_lenght)

		self.data={'Oil Temperature':self.oil_temp, 'Intake temperature':self.intake_temp\
			, 'Coolant Temperature':self.coolant_temp, 'RPM':self.rpm, 'Speed':self.speed\
			, 'Throttle Position':self.throttle_pos}
		# Initial values
		self.times.append(time.time())
		self.oil_temp.append(random.randrange(180,230))
		self.intake_temp.append(random.randrange(95,115))
		self.coolant_temp.append(random.randrange(170,220))
		self.rpm.append(random.randrange(1000,9500))
		self.speed.append(random.randrange(30,140))
		self.throttle_pos.append(random.randrange(10,90))

	def update(self):
		""" Generate new data """
		self.times.append(time.time())
		for key in self.data:
			self.data[key].append(self.data[key][-1]+self.data[key][-1]*random.uniform(-0.0001,0.0001))


DATA = VehicleData()
APP = dash.Dash('vehicle-data')
APP.layout = html.Div([html.Div([html.H2('Vehicle Data', style={'float':'left'})])\
	, dcc.Dropdown(id='vehicle-data-name', options=[{'label': s, 'value':s} for s in DATA.data.keys()]\
		, value=['RPM'], multi=True)\
	, html.Div(children=html.Div(id='graphs'), className='row')\
	, dcc.Interval(id='graph-update', interval=1000, n_intervals=0)]\
	, className='container', style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})

@APP.callback(dash.dependencies.Output('graphs', 'children')\
	, [dash.dependencies.Input('vehicle-data-name', 'value')\
	, dash.dependencies.Input('graph-update', 'n_intervals')])
def update_graph(data_names, _):
	""" Get graph to display """
	graphs = []
	DATA.update()
	if len(data_names) > 2:
		class_choice = 'col s12 m6 14'
	elif len(data_names) == 2:
		class_choice = 'col s12 m6 16'
	else:
		class_choice = 'col s12'

	for names in data_names:
		data = go.Scatter(x=list(DATA.times), y=list(DATA.data[names])\
			, name='Scatter', fill='tozeroy', fillcolor='#6897bb')
		graphs.append(html.Div(dcc.Graph(id=names, animate=True\
			, figure={'data':[data], 'layout': go.Layout(xaxis=dict(range=[min(DATA.times), max(DATA.times)])\
				, yaxis=dict(range=[min(DATA.data[names]), max(DATA.data[names])])\
				, margin={'l':50,'r':1,'t':45,'b':1}, title='{}'.format(names))})\
			, className=class_choice))
	return graphs


EXTERNAL_CSS = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css']
for css in EXTERNAL_CSS:
	APP.css.append_css({'external_url': css})

EXTERNAL_JS = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in EXTERNAL_JS:
    APP.scripts.append_script({'external_url': js})


if __name__ == '__main__':
	APP.run_server(debug=True)
