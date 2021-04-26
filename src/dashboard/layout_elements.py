from pathlib import Path

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from .assets.styles import Styles
from .table import holdings

sspath = Path(__file__).parent / "saved_stocks"


class Elements:
    """Individual web elements"""

    # ------ CONTENT WRAPER ------ #
    content = html.Div(id="page-content", style=Styles.content)

    # ------ SIDEBAR ------ #
    sidebar = html.Div(
        [
            html.H2("Controls", className="display-4"),
            html.Hr(),
            html.P("Just enter a stock ticker below", className="lead"),
            dcc.Input(
                id="ticker-input", type="text", placeholder="Input Ticker", className="input-group mb-3 form-control"
            ),
            dbc.Button("Add/Remove Company", id="ticker-button", n_clicks=0, style=Styles.button),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Watchlist", href="/Watchlist", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=Styles.side_nav,
    )

    header = html.Div(
        [
            html.H1("Financial Stocks Dashboard"),
            html.Hr(),
            html.P("Type a stock ticker into the sidebar to lookup it's price", className="lead"),
        ]
    )

    # ------ SINGLE STOCK SINGLE DAY CHANGE TICKER ------ #
    day_change = dbc.Container(
        [
            dbc.Row(
                [
                    dcc.Graph(id="day-change-indicator", figure={}, config={"displayModeBar": False},),
                    dcc.Interval(id="update", n_intervals=0, interval=1000 * 5),
                ]
            )
        ]
    )

    # ------ SINGLE STOCK GRAPH ------ #
    stock_price_graph = html.Div([dcc.Graph(id="stock-price-graph")], style={"width": 800})

    # ------ MULTI GRAPH HEADER ------ #
    multi_line_graph_header = html.Div(
        [
            html.H1("Mutli-Stock Graph", className="text-primary mb-4"),
            html.Hr(),
            html.P("Shows a graph of all stocks that have been searched and saved to disc", className="lead"),
        ]
    )

    # ------ MULTI GRAPH ------ #
    multi_line_graph = dbc.Container(
        [
            dbc.Row(
                [
                    dcc.Dropdown(
                        id="saved-stocks",
                        multi=True,
                        value=[k.resolve().stem for k in sspath.glob("*.csv")],
                        options=[{"label": x, "value": x} for x in [k.resolve().stem for k in sspath.glob("*.csv")]],
                    ),
                ],
                style={"width": 500},
            ),  # attempted to make dropdown minimum width :/
            dbc.Row(
                [dcc.Graph(id="multi-stock-graph", figure={})], style={"width": 800}
            ),  # Horizontal:start,center,end,between,around
        ],
        fluid=True,
    )

    # ------ HOLDINGS HEADER ------ #
    holding_header = html.Div(
        [
            html.H3("My Holdings Table"),
            html.Hr(),
            # html.P("Type a stock ticker into the sidebar to lookup it's price", className="lead")
        ]
    )

    # ------ HOLDINGS TABLE ------ #
    holding_table = dash_table.DataTable(
        id="ticker-table",
        columns=[{"name": i, "id": i} for i in holdings.df.columns],
        data=holdings.df.to_dict("records"),
        style_table=Styles.table,
    )

    # ------ HOLDINGS PIE ------ #
    holdings_pie = dcc.Graph(id="holdings-pie", figure={})
