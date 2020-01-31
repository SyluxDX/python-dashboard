""" Random dash """
from collections import namedtuple
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import yfinance as yf
from subs_data import SubscriberData
import google_api

SUBS = SubscriberData()
TIMER = 60 * 1000
APP = dash.Dash(__name__)
STOCKDATA = namedtuple('StockData', 'name index values')

def get_stock_data(name, period='1d', interval='1m'):
    """ Get stock data from Yahoo! Finance """
    stock = yf.Ticker(name)
    data = stock.history(period, interval)

    return STOCKDATA(stock.info['longName'],\
        data.Close.index.values,\
        data.Close.values)

# Page Layout
APP.layout = html.Div([dcc.Graph(id='stock-graph', animate=True)\
    , html.Div(id='wrapper'\
        , children=[html.Img(id='logo', src=APP.get_asset_url('logo.png')\
                , style={'vertical-align': 'top', 'display': 'inline-block'})\
            , dcc.Graph(id='subs-graph', animate=True\
                    , style={'width': '60%', 'display': 'inline-block'})\
            , dash_table.DataTable(id='search-table'\
                , style_as_list_view=True\
                , style_header={'backgroundColor': 'rgb(30, 30, 30)'\
                    , 'fontWeight': 'bold'\
                    , 'fontFamily': 'sans-serif'}\
                , style_cell={'backgroundColor': 'rgb(50, 50, 50)'\
                    , 'color': 'white'\
                    , 'padding': '10px'\
                    , 'fontFamily': 'sans-serif'})\
            , dcc.Interval(id='updates', interval=TIMER, n_intervals=0)])])

@APP.callback([dash.dependencies.Output('stock-graph', 'figure')\
    , dash.dependencies.Output('subs-graph', 'figure')\
    , dash.dependencies.Output('search-table', 'columns')\
    , dash.dependencies.Output('search-table', 'data')]\
    , [dash.dependencies.Input('updates', 'n_intervals')])
def update_data(_):
    """ Update Dash data """
    # Update stock
    data = get_stock_data(STOCK)
    stock_update = {'data':[{'x': data.index, 'y': data.values, 'type': 'line', 'name':data.name}]\
        , 'layout': {'title': data.name, 'yaxis': {'title':'USD'}\
            , 'paper_bgcolor': '#000000', 'plot_bgcolor': '#000000'\
            , 'font': {'color': '#FFFFFF'}\
            , 'xaxis': {'gridcolor': '#333333', 'linecolor': '#cccccc'}\
            , 'yaxis': {'gridcolor': '#333333', 'linecolor': '#cccccc'}}}

    # Update Subs count
    SUBS.add_data_points(google_api.get_sub_count())
    data = SUBS.get_data_points()
    yrange = [min(data[1]+data[2]+data[3])*0.9, max(data[1]+data[2]+data[3])*1.1]
    subs_udpate = {'data':[\
            {'x':data[0], 'y':data[3], 'type':'line', 'name':'Mean', 'marker':{'color': 'red'}}\
            , {'x':data[0], 'y':data[2], 'type':'bar', 'name':'Min', 'marker':{'color': 'green'}}\
            , {'x':data[0], 'y':data[1], 'type':'bar', 'name':'Max', 'marker':{'color': 'orange'}}]\
            , 'layout':{'title':'Subscribers Count for {}'.format(google_api.CHANNEL)\
                , 'paper_bgcolor': '#000000', 'plot_bgcolor': '#000000'\
                , 'font': {'color': '#FFFFFF'}\
                , 'xaxis': {'gridcolor': '#333333', 'linecolor': '#cccccc'}\
                , 'yaxis': {'gridcolor': '#333333', 'linecolor': '#cccccc'}\
                , 'yaxis':{'range':yrange}
                }}

    # Update Top Search
    data = google_api.get_google_trends().head(10)
    table_columns = [{"name": i, "id": i} for i in data.columns]
    table_data = data.to_dict('rows')

    return stock_update, subs_udpate, table_columns, table_data


if __name__ == '__main__':
    google_api.get_channel_logo()
    STOCK = 'TSLA'
    APP.run_server(debug=True, port=5000)
