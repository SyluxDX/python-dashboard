""" Part 2 Tutorial dash """
from datetime import datetime
import pandas_datareader as web
import dash
import dash_core_components as dcc
import dash_html_components as html


def get_stock_data(stock, exchange='iex', year=1, month=0, day=0):
    """ Get stock data from exchange """
    end = datetime.now()
    start = datetime(end.year-year, end.month-month, end.day-day)
    df = web.DataReader(stock, exchange, start, end)
    df.reset_index(inplace=True)
    df.set_index('date', inplace=True)
    return df

def create_dashboard():
    """ Create Dash dashboard """
    app = dash.Dash()
    stock = 'TSLA'
    data = get_stock_data(stock)
    app.layout = html.Div(children=[
        html.H1(children='Whoa, a graph')
        , html.Div(children='Making a stock graph!')
        , dcc.Graph(id='example-graph', figure={
            'data':[{'x': data.index, 'y': data.close, 'type': 'line', 'name':stock}]\
            , 'layout': {'title': stock, 'yaxis': {'title':'USD'}}
        })
    ])
    app.run_server(debug=True)

if __name__ == "__main__":
    create_dashboard()
