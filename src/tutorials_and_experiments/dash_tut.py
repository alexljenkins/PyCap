# code from:
# https://youtu.be/catwYsqkhqY

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

from alpha_vantage.timeseries import TimeSeries

# -------------------------------------------------------------------------------
# Set up initial key and financial category

# key = '7FEDJMHY3CM2KPEC' # Your API Key
# # https://github.com/RomelTorres/alpha_vantage
# # Chose your output format or default to JSON (python dict)
# ts = TimeSeries(key, output_format='pandas') # 'pandas' or 'json' or 'csv'
# ttm_data, ttm_meta_data = ts.get_intraday(symbol='TTM',interval='1min', outputsize='compact')
# df = ttm_data.iloc[:50].copy()
# df=df.transpose()
# df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
#                  "4. close":"close","5. volume":"volume"},inplace=True)
# df=df.reset_index().rename(columns={'index': 'indicator'})
# df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
# df = df[df['indicator']!='volume']


# df.to_csv("data2.csv", index=False)
# exit()


# df = df[df.indicator.isin(['high'])]
# df['date'] = pd.to_datetime(df['date'])
# two_recent_times = df['date'].nlargest(2)
# df = df[df['date'].isin(two_recent_times.values)]
# recent_high = df['rate'].iloc[0]
# older_high = df['rate'].iloc[1]
# print(recent_high, older_high)


dff = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/Financial/data.csv")
dff = dff[dff.indicator.isin(['high'])]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                        dbc.Row([
                            dbc.Col([
                                html.P("CHANGE (1D)", className="ml-3")
                            ],width={'size':5, 'offset':1}),

                            dbc.Col([
                                dcc.Graph(id='indicator-graph', figure={},
                                          config={'displayModeBar':False},
                                          )
                            ], width={'size':3,'offset':2})
                        ]),
                ]
            )
        ], width=6)
    ], justify='center'),
    dcc.Interval(id='update', n_intervals=0, interval=1000*5)
])

# Indicator Graph
@app.callback(
    Output('indicator-graph', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    dff_rv = dff.iloc[::-1]
    day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]

    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':12})
    fig.update_layout(height=30, width=70)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')

    return fig

if __name__=='__main__':
    app.run_server(debug=True, port=8000)

