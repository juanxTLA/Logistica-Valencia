# -*- coding: utf-8 -*-
import os

import dash
from dash import html
from dotenv import load_dotenv

from app import create_app

load_dotenv()
app = create_app()
dash_app = dash.Dash(__name__, server=app, url_base_pathname="/ayuda-valencia/")
dash_app.layout = html.Div([html.H1("Bienvenidos a la página de inicio de Pura")])

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
