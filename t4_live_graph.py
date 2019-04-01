""" Part 1 Tutorial dash """
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

# Random data
X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)

APP = dash.Dash(__name__)
APP.layout = html.Div([dcc.Graph(id='live-graph', animate=True)\
	, dcc.Interval(id='graph-update', interval=1000, n_intervals=0)])

@APP.callback(dash.dependencies.Output('live-graph', 'figure')\
	, [dash.dependencies.Input('graph-update', 'n_intervals')])
def update_graph_scatter(_):
	""" Generate random data """
	X.append(X[-1]+1)
	Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
	data = plotly.graph_objs.Scatter(x=list(X), y=list(Y), name='Scatter', mode='lines+markers')

	return {'data':[data]\
	, 'layout': go.Layout(xaxis=dict(range=[min(X),max(X)]), yaxis=dict(range=[min(Y),max(Y)]))}


if __name__ == '__main__':
	APP.run_server(debug=True)
