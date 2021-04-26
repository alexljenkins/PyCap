import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Union

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from pandas_datareader import data as web

from src.dashboard.layout_elements import Elements
from src.dashboard.assets.styles import Styles
from src.dashboard.table import holdings

df = pd.DataFrame()
df_of_stocks = pd.DataFrame()
saved_stocks_path = Path(__file__).parent / "src" / "dashboard" / "saved_stocks"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([dcc.Location(id="url"), Elements.sidebar, Elements.content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname: str) -> dbc.Container:
    """Web display wrapper for each page."""
    if pathname == "/":
        # return GRAPHS
        return dbc.Container(
            [
                dbc.Row(Elements.header),
                dbc.Row(Elements.day_change),
                dbc.Row(Elements.stock_price_graph),
                dbc.Row(Elements.holding_header),
                dbc.Row(Elements.holding_table),
                dbc.Row(Elements.holdings_pie),
            ]
        )

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


@app.callback(Output("stock-price-graph", "figure"), [Input("ticker-input", "value")])
def update_graph(ticker: str) -> Dict[str, Union[List[Dict[str, pd.Series]], Dict[str, str]]]:
    """ Uses Yahoo API to get the stock ticker price from the start of 2000 to yesterday and returns it in Dash format """
    global df
    df = web.DataReader(ticker, "yahoo", datetime.datetime(2000, 1, 1), datetime.datetime.now())
    df.to_csv(saved_stocks_path / f"{ticker}.csv", index=True)
    return {"data": [{"x": df.index, "y": df.Close}], "layout": Styles.stock_price_graph}


# Indicator Graph
@app.callback(Output("day-change-indicator", "figure"), Input("update", "n_intervals"))
def day_change_indicator(ticker: str) -> go.Figure:
    """ Returns the last day change indicator for the given stock """
    figure = go.Figure(
        go.Indicator(
            mode="delta",
            value=df.iloc[-1]["Close"],
            delta={"reference": df.iloc[-1]["Open"], "relative": True, "valueformat": ".2%"},
        )
    )
    figure.update_traces(delta_font={"size": 12})
    figure.update_layout(height=30, width=70)

    if df.iloc[-1]["Close"] >= df.iloc[-1]["Open"]:
        figure.update_traces(delta_increasing_color="green")
    elif df.iloc[-1]["Close"] < df.iloc[-1]["Open"]:
        figure.update_traces(delta_decreasing_color="red")

    return figure

# Multiple Line Chart DROPDOWN MENU
@app.callback(
    Output("saved-stocks", "options"),
    Input("saved-stocks", "value")
)
def update_multi_ticker_dropdown(saved_stocks: List[str]) -> List[Dict[str, str]]:
    """ Loads any previously saved stocks and returns a multi-stock graph of stock prices over time"""
    # look again for new files
    revised_saved_stocks = [k.resolve().stem for k in saved_stocks_path.glob("*.csv")]
    
    return [{"label": x, "value": x} for x in revised_saved_stocks]


# Multiple Line Charts
@app.callback(Output("multi-stock-graph", "figure"), Input("saved-stocks", "value"))
def update_multi_ticker_graph(saved_stocks: List[str]) -> go.Figure:
    """ Loads any previously saved stocks and returns a multi-stock graph of stock prices over time"""
    fig = go.Figure()
    for stock in saved_stocks:
        stock_df = pd.read_csv(saved_stocks_path / f"{stock}.csv")
        if not len(stock_df.index) > 5:
            print(f"Skipping {stock}")
            continue
        fig.add_trace(go.Scatter(x=stock_df["Date"], y=stock_df["Close"], name=stock))
    fig.update_layout(legend_title_text="Stocks", width=800, plot_bgcolor="#fff", showlegend=False)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Stock Price")

    return fig


# HOLDINGS TABLE UPDATE
@app.callback(
    Output("ticker-table", "data"),
    Output("ticker-table", "columns"),
    Input("ticker-table", "data"),
    Input("ticker-table", "columns"),
    Input("ticker-button", "n_clicks"),
    Input("ticker-input", "value"),
)
def add_stock(
    rows: List[Dict[str, Union[str, float, int]]],
    columns: List[Dict[str, Union[str, bool]]],
    n_clicks: int,
    ticker: str,
) -> Tuple[dict, dict]:
    """ Adds a stock to the holdings table (and corresponding pie chart) """
    # update only on button click
    if n_clicks != holdings.clicks:
        # removes user input from table
        if ticker in holdings.stocks:
            holdings.df = holdings.df[holdings.df["Ticker"] != ticker]
            holdings.stocks.remove(ticker)
            holdings.clicks = n_clicks

        # adds user input to table
        elif not ticker in holdings.stocks:
            holdings.stocks += [ticker]
            holdings.update_stocks_current_price()
            holdings.clicks = n_clicks

    # Update stocks owned on every call
    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    holdings.update_stock_quant(df["Owned"])

    # Update holdings value
    holdings.update_holdings_value()

    return holdings.df.to_dict("records"), holdings.get_column_dict()


# HOLDINGS PIE UPDATE
@app.callback(Output("holdings-pie", "figure"), Input("ticker-table", "data"), Input("ticker-table", "columns"))
def holdings_pie(rows: List[Dict[str, Union[str, float, int]]], columns: List[Dict[str, Union[str, bool]]]) -> px.pie:
    """ Returns a pie chart of current stock holdings """
    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    fig = px.pie(df, values="Total Value", names="Ticker")
    return fig


if __name__ == "__main__":
    app.run_server("0.0.0.0", port=8050, debug=True)
