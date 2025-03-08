# -*- coding: utf-8 -*-
import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_auth import BasicAuth
from dotenv import load_dotenv

from app import create_app
from db_handler import validate_user

load_dotenv()
app = create_app()
app.secret_key = os.urandom(24).hex()
dash_app = dash.Dash(
    __name__, server=app, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
BasicAuth(dash_app, auth_func=validate_user)
dash_app.title = "VASupply"
dash_app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            style={
                "position": "fixed",
                "top": "0",
                "right": "0",
                "left": "0",
                "bottom": "0",
                "zIndex": "-1",
                "backgroundColor": "#defcbb",
                "height": "100vh",
                "width": "100%",
                "font-family": "Montserrat, sans-serif",
            }
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
