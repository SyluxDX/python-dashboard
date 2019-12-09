""" Part 1 Tutorial dash """
import random
from collections import deque
import dash
import dash_core_components as dcc
import dash_html_components as html
# import plotly
import pandas
import plotly.graph_objs as pgo

# Random data
X = deque(maxlen=20)
Y = deque(maxlen=20)
Y2 = deque(maxlen=20)
X.append(1)
Y.append(1)
Y2.append(1)

APP = dash.Dash(__name__)
APP.layout = html.Div([dcc.Graph(id='live-graph', animate=True)\
    , dcc.Graph(id='live2-graph', animate=True)\
    , dcc.Interval(id='graph-update', interval=1000, n_intervals=1000)])

@APP.callback([dash.dependencies.Output('live-graph', 'figure')\
    , dash.dependencies.Output('live2-graph', 'figure')]\
    , [dash.dependencies.Input('graph-update', 'n_intervals')])
def update_graph_scatter(_):
    """ Generate random data """
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1, 0.1))
    Y2.append(Y2[-1]+Y2[-1]*random.uniform(-0.1, 0.1))

    data = pgo.Scatter(x=list(X), y=list(Y), name='Scatter', mode='lines+markers')
    figure = {'data':[data]\
	, 'layout': pgo.Layout(xaxis=dict(range=[min(X), max(X)]), yaxis=dict(range=[min(Y), max(Y)]))}

    data = pgo.Scatter(x=list(X), y=list(Y2), name='Scatter', mode='lines+markers')
    figure2 = {'data':[data]\
	, 'layout': pgo.Layout(xaxis=dict(range=[min(X), max(X)]), yaxis=dict(range=[min(Y2), max(Y2)]))}

    return figure, figure2


if __name__ == '__main__':
    APP.run_server(debug=True, port=5000)
