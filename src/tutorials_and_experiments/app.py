import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from pandas_datareader import data as web
from datetime import datetime

app = dash.Dash('Hello World')

app.layout = html.Div([
    dcc.Input(
        id='ticker-input',
        type='text',
        placeholder="input ticker"
    ),
    dcc.Dropdown(
        id='interval-dropdown',
        options=[
            {'label': 'Yearly', 'value': 'Yearly'},
            {'label': 'Monthly', 'value': 'Monthly'},
            {'label': 'Daily', 'value': 'Daily'}
        ],
        value='Yearly'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})

@app.callback(Output('my-graph', 'figure'), [Input('ticker-input', 'value')])
def update_graph(ticker):
    df = web.DataReader(
        ticker,
        'yahoo',
        datetime(2000, 1, 1),
        datetime.now()
    )
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }

# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server()