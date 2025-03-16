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


dash.register_page(__name__, path="/afectados", name="Afectados")

layout = html.Div(
    [
        html.H1("Gestión de Afectados"),
        dash_table.DataTable(
            id="afectados-table",
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
            "Añadir Afectado",
            id="add-afectado-btn",
            n_clicks=0,
            style={"margin": "10px"},
        ),
        dcc.Input(id="new-afectado-name", type="text", placeholder="Nombre"),
        dcc.Input(id="new-afectado-email", type="email", placeholder="Email"),
        html.Div(id="output-afectados"),
    ],
    style={"margin": "30px"},
)


@callback(
    Output("afectados-table", "data"),
    Input("add-afectado-btn", "n_clicks"),
    State("new-afectado-name", "value"),
    State("new-afectado-email", "value"),
    State("afectados-table", "data"),
)
def add_user(n_clicks, name, email, rows):
    if n_clicks > 0 and name and email:
        new_id = max(row["id"] for row in rows) + 1 if rows else 1
        new_row = {"id": new_id, "nombre": name, "email": email}
        rows.append(new_row)
        dummy_data.append(new_row)
    return rows


@callback(Output("output-afectados", "children"), Input("afectados-table", "data"))
def update_users(rows):
    global dummy_data
    dummy_data = rows
    return "Afectados actualizados"
