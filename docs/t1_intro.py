""" Part 1 Tutorial dash """
import dash
import dash_core_components as dcc
import dash_html_components as html

APP = dash.Dash()
# APP.layout = html.Div('Dash Tutorials')
APP.layout = html.Div(children=[html.H1(children='Dash Tutorial')\
    , dcc.Graph(id='example'\
        , figure={'data':[{'x':[1, 2, 3, 4, 5], 'y':[9, 6, 2, 1, 7], 'type':'line', 'name':'Boars'}\
            , {'x':[1, 2, 3, 4, 5], 'y':[9, 7, 2, 7, 3], 'type':'bar', 'name':'Cars'}]\
            , 'layout':{'title':'Basic Dash Example'}})])

if __name__ == "__main__":
    APP.run_server(debug=True)
