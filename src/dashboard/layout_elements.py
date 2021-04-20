from pathlib import Path

import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

from styles import Styles
from table import holdings

class Elements:
    # ------ CONTENT WRAPER ------ #
    content = html.Div(id="page-content", style=Styles.content)

    # ------ SIDEBAR ------ #
    sidebar = html.Div(
        [
            html.H2("Sidebar", className="display-4"),
            html.Hr(),
            html.P(
                "A simple sidebar layout with navigation links", className="lead"
            ),
            dcc.Input(
                id='ticker-input',
                type='text',
                placeholder="Input Ticker",
                className="input-group mb-3 form-control"
            ),
            html.Button(
                'Add/Remove Company',
                id = 'ticker-button',
                n_clicks = 0,
                style=Styles.button
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Holdings", href="/holdings", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=Styles.side_nav,
    )

    # ------ SINGLE STOCK SINGLE DAY CHANGE TICKER ------ #
    day_change = dbc.Container([
        dbc.Row([dcc.Graph(id='day-change-indicator', figure={},
                            config={'displayModeBar':False},
                            ),
        dcc.Interval(id='update', n_intervals=0, interval=1000*5)
    ])])
    
    # ------ SINGLE STOCK GRAPH ------ #
    stock_price_graph = html.Div([dcc.Graph(id='stock-price-graph')], style={'width': 800})

    # ------ MULTI GRAPH ------ #
    multi_line_graph = dbc.Container([
        dbc.Row(
            dbc.Col(html.H1("Mutli-Stock Graph",
                            className='text-center text-primary mb-4'),
                    width=12)
        ),
        dbc.Row([
                dcc.Dropdown(id='saved-stocks', multi=True, value=[k.resolve().stem for k in Path("./saved_stocks").glob('*.csv')],
                            options=[{'label':x, 'value':x}
                                    for x in [k.resolve().stem for k in Path("./saved_stocks").glob('*.csv')]
                                ],
                            ),
        ], style={"width": 500}), # attempted to make dropdown minimum width :/
        dbc.Row([
                dcc.Graph(id='multi-stock-graph', figure={})
        ], style={'width': 800}),  # Horizontal:start,center,end,between,around
    ], fluid=True)

    # ------ BUTTON ------ #
    # NOT YET IMPLEMENTED
    # button = html.Button('Add/Remove Company', id = 'ticker-button', n_clicks = 0)
    # ------ HOLDINGS TABLE ------ #
    holding_table = dash_table.DataTable(
        id = 'ticker-table',
        columns = [{"name": i, "id": i} for i in holdings.df.columns],
        data = holdings.df.to_dict('records')
    )