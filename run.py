# -*- coding: utf-8 -*-
import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_auth import BasicAuth
from dotenv import load_dotenv

from app import create_app
from pages.components import navbar, register_navbar_callbacks

load_dotenv()
app = create_app()
app.secret_key = os.urandom(24).hex()
dash_app = dash.Dash(
    __name__, server=app, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
BasicAuth(dash_app, auth_func=app.config["sqlite_handler"].validate_user)

# Pass the database handler to the Dash app using the server object
app.config["sqlite_handler"] = app.config["sqlite_handler"]

dash_app.title = "VASupply"
dash_app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        html.Div(
            style={
                "position": "fixed",
                "top": "0",
                "right": "0",
                "left": "0",
                "bottom": "0",
                "zIndex": "-1",
                "backgroundColor": "#ffffff",
                "height": "100vh",
                "width": "100%",
                "font-family": "Montserrat, sans-serif",
            }
        ),
        dash.page_container,
    ]
)

register_navbar_callbacks(dash_app)

if __name__ == "__main__":
    # app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
    app.run(debug=True)
