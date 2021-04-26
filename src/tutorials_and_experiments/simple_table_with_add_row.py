import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import pandas_datareader as web
from dash.dependencies import Input, Output


class Var:
    def __init__(self):
        self._clicks = 0
        self.stocks = ["TSLA", "AAPL"]
        self.df = None
        self.update_stocks_current_price()

    @property
    def clicks(self) -> int:
        return self._clicks

    @clicks.setter
    def clicks(self, new_clicks: int) -> None:
        if isinstance(new_clicks, int):
            self._clicks = new_clicks

    def update_stocks_current_price(self):
        # Can't get yesterdays close price on Monday/Weekends
        try:
            start = datetime.datetime.today() - datetime.timedelta(days=1)
            end = datetime.datetime.today()
            d = web.DataReader(self.stocks, "yahoo", start, end)
        except:
            start = datetime.datetime.today() - datetime.timedelta(days=3)
            end = datetime.datetime.today()
            d = web.DataReader(self.stocks, "yahoo", start, end)

        self.df = d["Close"].T
        self.df.reset_index(inplace=True)
        # Ensure there's only 2 columns
        self.df = self.df[self.df.columns[0:2]]
        self.df.columns = ["Ticker", "Close"]
        # self.df.drop('remove', axis = 1, inplace = True)
        self.df["Owned"] = 0

    def update_stock_quant(self, owned_series=None):
        self.df["Owned"] = 0
        if isinstance(owned_series, pd.Series):
            self.df["Owned"] = owned_series

    def get_column_dict(self):
        # TODO: could try turn this into a 1 liner with if else inside list comp
        d = [
            {"name": i, "id": i, "editable": False, "renamable": False, "deletable": False} for i in current.df.columns
        ]
        for column in d:
            if column["name"] == "Owned":
                column["editable"] = True
                column["renamable"] = True
                column["deletable"] = True
        return d

    def update_holdings_value(self):
        self.df["Total Value"] = round(self.df["Close"] * self.df["Owned"].astype(float), 2)


@app.callback(
    Output("ticker-table", "data"),
    Output("ticker-table", "columns"),
    Input("ticker-table", "data"),
    Input("ticker-table", "columns"),
    Input("ticker-button", "n_clicks"),
    Input("ticker-input", "value"),
)
def add_stock(rows, columns, n_clicks, ticker):
    # update only on button click
    if n_clicks != current.clicks:
        # removes user input from table
        if ticker in current.stocks:
            current.df = current.df[current.df["Ticker"] != ticker]
            current.stocks.remove(ticker)
            current.clicks = n_clicks

        # adds user input to table
        elif not ticker in current.stocks:
            current.stocks += [ticker]
            current.update_stocks_current_price()
            current.clicks = n_clicks

    # Update stocks owned on every call
    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    current.update_stock_quant(df["Owned"])

    # Update holdings value
    current.update_holdings_value()

    return current.df.to_dict("records"), current.get_column_dict()


if __name__ == "__main__":
    app.run_server(debug=True)
    current = Var()

    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            dcc.Input(id="ticker-input", placeholder="Enter a Company Ticker...", value="", style={"padding": 10}),
            html.Button("Add/Remove Company", id="ticker-button", n_clicks=0),
            dash_table.DataTable(
                id="ticker-table",
                columns=[{"name": i, "id": i} for i in current.df.columns],
                data=current.df.to_dict("records"),
            ),
        ]
    )
