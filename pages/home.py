import dash
from dash import dcc, html

dash.register_page(__name__, path="/home", name="VASupply")

layout = html.Div([dcc.Location(id="url", refresh=False), html.H1("Home of VASupply")])
