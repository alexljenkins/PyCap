import dash
import dash_table
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

from table import holdings
from layout_elements import Elements

df = pd.DataFrame()
df_of_stocks = pd.DataFrame()

app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])
# app.config['suppress_callback_exceptions']=True

app.layout = html.Div([dcc.Location(id="url"), Elements.sidebar, Elements.content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        # return GRAPHS
        return dbc.Container([
            dbc.Row(Elements.header),
            dbc.Row(Elements.day_change),
            dbc.Row(Elements.stock_price_graph),
            dbc.Row(Elements.holding_header),
            dbc.Row(Elements.holding_table)
        ])

    elif pathname == "/Watchlist":
        return dbc.Container([dbc.Row([Elements.multi_line_graph_header, Elements.multi_line_graph])])
    
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
        'layout': {'margin': {'l': 0, 'r': 0, 't': 20, 'b': 30},
        'width': '800'}
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

@app.callback(
    Output('ticker-table', 'data'),
    Output('ticker-table', 'columns'),
    Input('ticker-table', 'data'),
    Input('ticker-table', 'columns'),
    Input('ticker-button', 'n_clicks'),
    Input('ticker-input', 'value')
)
def add_stock(rows, columns, n_clicks, ticker):
    # update only on button click
    if n_clicks != holdings.clicks:
        # removes user input from table
        if ticker in holdings.stocks:
            holdings.df = holdings.df[holdings.df['Ticker'] != ticker]
            holdings.stocks.remove(ticker)
            holdings.clicks = n_clicks
        
        # adds user input to table
        elif not ticker in holdings.stocks:
            holdings.stocks += [ticker]
            holdings.update_stocks_current_price()
            holdings.clicks = n_clicks
    
    # Update stocks owned on every call
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    holdings.update_stock_quant(df["Owned"])

    # Update holdings value
    holdings.update_holdings_value()

    return holdings.df.to_dict('records'), holdings.get_column_dict()

if __name__ == '__main__':
    app.run_server(debug=True)