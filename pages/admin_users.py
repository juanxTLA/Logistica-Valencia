import dash
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html


# Dummy data function
def fetch_users():
    global dummy_data
    dummy_data = [
        {"id": 1, "nombre": "Juan Perez", "email": "juan.perez@example.com"},
        {"id": 2, "nombre": "Maria Lopez", "email": "maria.lopez@example.com"},
    ]
    return pd.DataFrame(dummy_data)


dash.register_page(__name__, path="/admin_usuarios", name="Usuarios")

layout = html.Div(
    [
        html.H1("Gestión de Usuarios"),
        dash_table.DataTable(
            id="usuarios-table",
            columns=[
                {"name": "ID", "id": "id", "editable": False},
                {"name": "Nombre", "id": "nombre", "editable": True},
                {"name": "Email", "id": "email", "editable": True},
            ],
            data=fetch_users().to_dict("records"),
            row_deletable=True,
            editable=True,
        ),
        html.Button(
            "Añadir Usuario", id="add-user-btn", n_clicks=0, style={"margin": "10px"}
        ),
        dcc.Input(id="new-user-name", type="text", placeholder="Nombre"),
        dcc.Input(id="new-user-email", type="email", placeholder="Email"),
        html.Div(id="output-users"),
    ],
    style={"margin": "30px"},
)


@callback(
    Output("usuarios-table", "data"),
    Input("add-user-btn", "n_clicks"),
    State("new-user-name", "value"),
    State("new-user-email", "value"),
    State("usuarios-table", "data"),
)
def add_user(n_clicks, name, email, rows):
    if n_clicks > 0 and name and email:
        new_id = max(row["id"] for row in rows) + 1 if rows else 1
        new_row = {"id": new_id, "nombre": name, "email": email}
        rows.append(new_row)
        dummy_data.append(new_row)
    return rows


@callback(Output("output-users", "children"), Input("usuarios-table", "data"))
def update_users(rows):
    global dummy_data
    dummy_data = rows
    return "Usuarios actualizados"
