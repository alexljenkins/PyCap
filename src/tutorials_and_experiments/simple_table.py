#%%
import dash
import dash_table
import pandas as pd
import pandas_datareader as web
import datetime


def get_stocks_current_price(stocks:list = ['TSLA', 'AAPL'], df:pd.DataFrame = None) -> pd.DataFrame:
    if isinstance(df, pd.DataFrame) and sorted(stocks) == sorted(df['Symbols']):
        return df
    start = datetime.datetime.today() - datetime.timedelta(days=1)
    end = datetime.datetime.today()
    d = web.DataReader(stocks, 'yahoo', start, end)
    df = d['Close'].T
    df.columns = ["Ticker"]
    df.reset_index(inplace=True)

    return df 



app = dash.Dash(__name__)

df = get_stocks_current_price()

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data = df.to_dict('records'),
)

if __name__ == '__main__':
    app.run_server(debug=True)


# %%
