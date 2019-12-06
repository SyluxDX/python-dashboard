""" Part 2 Tutorial dash """
import dash
# from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

APP = dash.Dash()
APP.layout = html.Div([dcc.Input(id='input', value='Enter something here', type='text')\
    , html.Div(id='output')])

@APP.callback(dash.dependencies.Output(component_id='output', component_property='children')\
    , [dash.dependencies.Input(component_id='input', component_property='value')])
def update_value(input_data):
    """ Updates values from with each keypress """
    return 'Input: {}'.format(input_data)

if __name__ == "__main__":
    APP.run_server(debug=True)
