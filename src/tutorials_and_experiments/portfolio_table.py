from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

STOCKS = [k.resolve().stem for k in Path("./saved_stocks").glob("*.csv")]
COLUMNS = ["ticker", "bought at", "current", "change"]


app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Input(
                    id="adding-rows-name", placeholder="Enter a Company Ticker...", value="", style={"padding": 10}
                ),
                html.Button("Add Company", id="editing-rows-button", n_clicks=0),
            ],
            style={"height": 50},
        ),
        dash_table.DataTable(
            id="adding-rows-table",
            columns=[{"name": column, "id": column, "deletable": False, "renamable": False} for column in COLUMNS],
            data=[{f"column-{i}": (len(STOCKS) + (i - 1) * 5) for i in range(1, 5)} for stock in STOCKS],
            editable=True,
            row_deletable=True,
            style_as_list_view=True,
        ),
        # dcc.Graph(id='adding-rows-graph')
    ]
)


@app.callback(
    Output("adding-rows-table", "data"),
    Input("editing-rows-button", "n_clicks"),
    State("adding-rows-table", "data"),
    State("adding-rows-table", "columns"),
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
        print(rows)
    return rows


# @app.callback(
#     Output('adding-rows-table', 'columns'),
#     Input('adding-rows-button', 'n_clicks'),
#     State('adding-rows-name', 'value'),
#     State('adding-rows-table', 'columns'))
# def update_columns(n_clicks, value, existing_columns):
#     if n_clicks > 0:
#         existing_columns.append({
#             'id': value, 'name': value,
#             'renamable': True, 'deletable': True
#         })
#     return existing_columns


# @app.callback(
#     Output('adding-rows-graph', 'figure'),
#     Input('adding-rows-table', 'data'),
#     Input('adding-rows-table', 'columns'))
# def display_output(rows, columns):
#     return {
#         'data': [{
#             'type': 'heatmap',
#             'z': [[row.get(c['id'], None) for c in columns] for row in rows],
#             'x': [c['name'] for c in columns]
#         }]
#     }


if __name__ == "__main__":
    app.run_server(debug=True)
