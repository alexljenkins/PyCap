import datetime
from typing import Dict, List, Union

import pandas as pd
import pandas_datareader as web


class HoldingsTable:
    """ Holdings Table Class to allow for adding, removing and editing stocks and quantity in the web app."""

    def __init__(self) -> None:
        """Sets TSLA and APPL as defaults stocks to show you how it would look. These can be removed with button."""
        self._clicks = 0
        self.stocks = ["TSLA", "AAPL"]
        self.df = None
        self.update_stocks_current_price()

    @property
    def clicks(self) -> int:
        """Returns the number of button clicks made by a user"""
        return self._clicks

    @clicks.setter
    def clicks(self, new_clicks: int) -> None:
        """Updates the number of clicks made by a user"""
        if isinstance(new_clicks, int):
            self._clicks = new_clicks
        else:
            raise (Exception("int required"))

    def update_stocks_current_price(self) -> None:
        """Uses Yahoo API to get yesterdays (or last trading days) closing stock price for all current stocks"""
        # Can't get yesterdays close price on Sunday/Monday
        try:
            start = datetime.datetime.today() - datetime.timedelta(days=1)
            end = datetime.datetime.today()
            d = web.DataReader(self.stocks, "yahoo", start, end)
        except Exception:
            start = datetime.datetime.today() - datetime.timedelta(days=3)
            end = datetime.datetime.today()
            d = web.DataReader(self.stocks, "yahoo", start, end)

        self.df = d["Close"].T
        self.df.reset_index(inplace=True)
        # Ensure there's only 2 columns
        while len(self.df.columns) > 2:
            self.df = self.df.iloc[:, :-1]
        self.df.columns = ["Ticker", "Close"]
        self.df["Owned"] = 0

    def update_stock_quant(self, owned_series: pd.Series = None) -> None:
        """ Updates the editable column in the stocks holdings table"""
        self.df["Owned"] = 0
        if isinstance(owned_series, pd.Series):
            self.df["Owned"] = owned_series

    def get_column_dict(self) -> List[Dict[str, Union[str, bool]]]:
        """ Returns the columns from the pandas dataframe of stock holdings as a list of dicts for Dash to create the table from.
        """
        # TODO: could try turn this into a 1 liner with if else inside list comp
        d = [
            {"name": i, "id": i, "editable": False, "renamable": False, "deletable": False} for i in holdings.df.columns
        ]
        for column in d:
            if column["name"] == "Owned":
                column["editable"] = True
                column["renamable"] = True
                column["deletable"] = True
        return d

    def update_holdings_value(self):
        """Multiplies 'Owned' by 'Close' columns to work out  holdings total current value for each stock.
        """
        self.df["Total Value"] = round(self.df["Close"] * self.df["Owned"].astype(float), 2)


holdings = HoldingsTable()
