import pandas as pd
from truth.truth import AssertThat

from ..dashboard.table import HoldingsTable

HOLDINGS = HoldingsTable()
T = pd.Series([5, 5, 5])


def test_update_stocks_current_price():
    HOLDINGS.stocks = ["TSLA", "AAPL", "GOOGL"]
    HOLDINGS.update_stocks_current_price()

    assert (HOLDINGS.df.columns == ["Ticker", "Close", "Owned"]).all()
    assert len(HOLDINGS.df.index) == 3


def test_clicks():
    HOLDINGS.clicks = 5
    assert HOLDINGS.clicks == 5
    HOLDINGS.clicks = 6
    assert HOLDINGS.clicks == 6


def test_clicks_error():
    with AssertThat(Exception).IsRaised():
        HOLDINGS.clicks = 5.0
    with AssertThat(Exception).IsRaised():
        HOLDINGS.clicks = "random"


def test_update_stock_quant():
    # 3 values because test_update_stocks_current_price has added an additional stock to the global HOLDINGS list
    HOLDINGS.update_stock_quant(T)
    assert (HOLDINGS.df["Owned"] == T).all()


def test_get_column_dict():
    """ Check that we build the correct layout for the table headers and allow only the Owned column to be edited """
    solution = [
        {"name": "Ticker", "id": "Ticker", "editable": False, "renamable": False, "deletable": False},
        {"name": "Close", "id": "Close", "editable": False, "renamable": False, "deletable": False},
        {"name": "Owned", "id": "Owned", "editable": True, "renamable": True, "deletable": True},
    ]
    d = HOLDINGS.get_column_dict()
    assert d == solution


def test_update_holdings_value():
    # since test_update_stock_quant has updated holdings to 5,5,5, simply check values match up
    HOLDINGS.update_holdings_value()
    solution = round(HOLDINGS.df["Close"] * T.astype(float), 2)
    assert (HOLDINGS.df["Total Value"] == solution).all()
