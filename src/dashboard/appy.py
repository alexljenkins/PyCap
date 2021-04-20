import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

from pathlib import Path
from pandas_datareader import data as web
import datetime
import pandas as pd

from styles import Styles

df = pd.DataFrame()
df_of_stocks = pd.DataFrame()

app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])


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
    add_button = dbc.Button("Add to Holdings", className="ml-5 input-group-append btn btn-outline-secondary")


app.layout = html.Div([dcc.Location(id="url"), Elements.sidebar, Elements.content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        # return GRAPHS
        return dbc.Container([
            dbc.Row([Elements.day_change]),
            dbc.Row([Elements.stock_price_graph]),
            dbc.Row([Elements.multi_line_graph])
        ])

    elif pathname == "/holdings":
        return html.P("This is the content of your holdings. Yay!")
    
    # 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(Output('stock-price-graph', 'figure'), [Input('ticker-input', 'value')])
def update_graph(ticker):
    global df
    df = web.DataReader(
        ticker,
        'yahoo',
        datetime.datetime(2000, 1, 1),
        datetime.datetime.now()
    )
    df.to_csv(f"saved_stocks/{ticker}.csv", index=True)
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }

# Indicator Graph
@app.callback(
    Output('day-change-indicator', 'figure'),
    Input('update', 'n_intervals')
)
def day_change_indicator(ticker):
    figure = go.Figure(go.Indicator(
        mode="delta",
        value=df.iloc[-1]['Close'],
        delta={'reference': df.iloc[-1]['Open'], 'relative': True, 'valueformat':'.2%'}))
    figure.update_traces(delta_font={'size':12})
    figure.update_layout(height=30, width=70)

    if df.iloc[-1]['Close'] >= df.iloc[-1]['Open']:
        figure.update_traces(delta_increasing_color='green')
    elif df.iloc[-1]['Close'] < df.iloc[-1]['Open']:
        figure.update_traces(delta_decreasing_color='red')

    return figure

# Multiple Line Charts
@app.callback(
    Output('multi-stock-graph', 'figure'),
    Input('saved-stocks', 'value')
)
def update_multi_ticker_graph(saved_stocks):
    fig = go.Figure()
    for stock in saved_stocks:
        stock_df = pd.read_csv(f"./saved_stocks/{stock}.csv")
        if not len(stock_df.index) > 5:
            print(f"skipping {stock}")
            continue
        fig.add_trace(go.Scatter(
            x = stock_df['Date'],
            y = stock_df['Close'],
            name = stock
        ))
    fig.update_layout(legend_title_text = "Stocks", width=800, plot_bgcolor="#fff", showlegend=False)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Stock Price")

    return fig

if __name__ == '__main__':
    # update_day_change(ticker='GOOGL')
    app.run_server(debug=True)