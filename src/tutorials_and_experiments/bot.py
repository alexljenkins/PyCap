### https://github.com/RomelTorres/alpha_vantage
from key import KEY

symbol = "GOOGL"


def intrday_timeseries(key, symbol):
    from alpha_vantage.timeseries import TimeSeries

    ts = TimeSeries(key=KEY, output_format="pandas", indexing_type="date")
    # Get json object with the intraday data and another with the call's metadata
    # data, meta_data = ts.get_intraday(symbol)
    data, meta_data = ts.get_daily(symbol)
    print(f"Data:\n{data}\nmeta_data:\n{meta_data}")


# intrday_timeseries(KEY, symbol)


def bollinger_bands(key, symbol):
    from alpha_vantage.techindicators import TechIndicators
    import matplotlib.pyplot as plt

    ti = TechIndicators(key=key, output_format="pandas")
    data, meta_data = ti.get_bbands(symbol=symbol, interval="60min", time_period=60)
    data.plot()
    plt.title("BBbands indicator for  MSFT stock (60 min)")
    plt.show()


# bollinger_bands(KEY, symbol)


def sector_performance_graph(key):
    from alpha_vantage.sectorperformance import SectorPerformances
    import matplotlib.pyplot as plt

    sp = SectorPerformances(key=key, output_format="pandas")
    data, meta_data = sp.get_sector()
    data["Rank A: Real-Time Performance"].plot(kind="bar")
    plt.title("Real Time Performance (%) per Sector")
    plt.tight_layout()
    plt.grid()
    plt.show()


# sector_performance_graph(KEY)


def crypto_currencies(key, symbol, market="CNY"):
    from alpha_vantage.cryptocurrencies import CryptoCurrencies
    import matplotlib.pyplot as plt

    cc = CryptoCurrencies(key=key, output_format="pandas")
    data, meta_data = cc.get_digital_currency_daily(symbol=symbol, market=market)
    data["4b. close (USD)"].plot()
    plt.tight_layout()
    plt.title("Daily close value for bitcoin (BTC)")
    plt.grid()
    plt.show()


crypto_currencies(KEY, "BTC")
