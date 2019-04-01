""" Part 3 Tutorial dash """
from datetime import datetime
import pandas_datareader as web
import dash
import dash_core_components as dcc
import dash_html_components as html


def get_stock_data(stock, exchange='iex', year=1, month=0, day=0):
    """ Get stock data from exchange """
    end = datetime.now()
    start = datetime(end.year-year, end.month-month, end.day-day)
    data_frame = web.DataReader(stock, exchange, start, end)
    data_frame.reset_index(inplace=True)
    data_frame.set_index('date', inplace=True)
    return data_frame


AAP = dash.Dash()
AAP.layout = html.Div(children=[
    html.H1(children='Symbol to graph')\
    , dcc.Input(id='input', value='', type='text')
    , html.Div(id='output-graph')])

@AAP.callback(
    dash.dependencies.Output(component_id='output-graph', component_property='children')\
        , [dash.dependencies.Input(component_id='input', component_property='value')])
def update_value(input_data):
    """ Get data? """
    input_data = input_data.upper()
    if not input_data:
        return None
    try:
        data = get_stock_data(input_data)
        return dcc.Graph(id='example-graph', figure={
            'data':[{'x': data.index, 'y': data.close, 'type': 'line', 'name':input_data}]\
                , 'layout': {'title': input_data, 'yaxis': {'title':'USD'}}
        })
    except KeyError:
        return 'Stock {} not found'.format(input_data)


if __name__ == "__main__":
    AAP.run_server(debug=True)
