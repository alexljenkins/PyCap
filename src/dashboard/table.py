import dash
import dash_table
import pandas as pd
import pandas_datareader as web
import datetime
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

class HoldingsTable:
    def __init__(self):
        self._clicks = 0
        self.stocks = ['TSLA', 'AAPL']
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
            d = web.DataReader(self.stocks, 'yahoo', start, end)
        except:
            start = datetime.datetime.today() - datetime.timedelta(days=3)
            end = datetime.datetime.today()
            d = web.DataReader(self.stocks, 'yahoo', start, end)
        
        self.df = d['Close'].T
        self.df.reset_index(inplace=True)
        # Ensure there's only 2 columns
        while len(self.df.columns) > 2:
            self.df = self.df.iloc[:,:-1]
        self.df.columns = ["Ticker", "Close"]
        self.df['Owned'] = 0
    
    def update_stock_quant(self, owned_series = None):
        self.df['Owned'] = 0
        if isinstance(owned_series, pd.Series):
            self.df['Owned'] = owned_series
    
    def get_column_dict(self):
        # TODO: could try turn this into a 1 liner with if else inside list comp
        d = [{"name": i, "id": i, "editable": False, 'renamable': False, 'deletable': False} for i in holdings.df.columns]
        for column in d:
            if column['name'] == "Owned":
                column['editable'] = True
                column['renamable'] = True
                column['deletable'] = True
        return d
    
    def update_holdings_value(self):
        self.df['Total Value'] = round(self.df['Close'] * self.df['Owned'].astype(float), 2)


# app = dash.Dash(__name__)
# app.config['suppress_callback_exceptions']=True
holdings = HoldingsTable()

# app.layout = html.Div([
#     dcc.Input(
#             id='ticker-input',
#             placeholder='Enter a Company Ticker...',
#             value='',
#             style={'padding': 10}
#         ),
#     html.Button('Add/Remove Company', id = 'ticker-button', n_clicks = 0),
#     dash_table.DataTable(
#         id = 'ticker-table',
#         columns = [{"name": i, "id": i} for i in holdings.df.columns],
#         data = holdings.df.to_dict('records')
#     )
# ])


# @app.callback(
#     Output('ticker-table', 'data'),
#     Output('ticker-table', 'columns'),
#     Input('ticker-table', 'data'),
#     Input('ticker-table', 'columns'),
#     Input('ticker-button', 'n_clicks'),
#     Input('ticker-input', 'value')
# )
# def add_stock(rows, columns, n_clicks, ticker):
#     # update only on button click
#     if n_clicks != holdings.clicks:
#         # removes user input from table
#         if ticker in holdings.stocks:
#             holdings.df = holdings.df[holdings.df['Ticker'] != ticker]
#             holdings.stocks.remove(ticker)
#             holdings.clicks = n_clicks
        
#         # adds user input to table
#         elif not ticker in holdings.stocks:
#             holdings.stocks += [ticker]
#             holdings.update_stocks_current_price()
#             holdings.clicks = n_clicks
    
#     # Update stocks owned on every call
#     df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#     holdings.update_stock_quant(df["Owned"])

#     # Update holdings value
#     holdings.update_holdings_value()

#     return holdings.df.to_dict('records'), holdings.get_column_dict()



if __name__ == '__main__':
    app.run_server(debug=True)