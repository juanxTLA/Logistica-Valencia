import dash
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html
from flask import current_app, session

dash.register_page(__name__, path="/admin_usuarios", name="Usuarios")

layout = html.Div(id="admin-users-content")


@callback(Output("admin-users-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if session.get("user_group") == "Admin":
        db_handler = current_app.config["sqlite_handler"]
        users_data = pd.DataFrame(db_handler.fetch_users())
        return html.Div(
            [
                html.H1("Gestión de Usuarios"),
                dash_table.DataTable(
                    id="usuarios-table",
                    columns=[
                        {"name": "Nombre", "id": "nombre", "editable": True},
                        {"name": "Email", "id": "email", "editable": True},
                        {"name": "Rol", "id": "rol", "editable": True},
                    ],
                    data=users_data.to_dict("records"),
                    row_deletable=True,
                    editable=True,
                    filter_action="native",
                    filter_options={"placeholder_text": "filtrar por ..."},
                ),
                html.Button(
                    "Añadir Usuario",
                    id="add-user-btn",
                    n_clicks=0,
                    style={"margin": "10px"},
                ),
                dcc.Input(id="new-user-name", type="text", placeholder="Nombre"),
                dcc.Input(
                    id="new-user-password", type="password", placeholder="Contraseña"
                ),
                dcc.Input(id="new-user-email", type="email", placeholder="Email"),
                dcc.Input(id="new-user-rol", type="text", placeholder="Rol"),
                html.Div(id="output-users"),
            ],
            style={"margin": "30px"},
        )
    else:
        return html.Div("No tiene permisos para acceder a esta página.")


@callback(
    Output("usuarios-table", "data"),
    Input("add-user-btn", "n_clicks"),
    State("new-user-name", "value"),
    State("new-user-password", "value"),
    State("new-user-email", "value"),
    State("new-user-rol", "value"),
    State("usuarios-table", "data"),
)
def add_user(n_clicks, name, password, email, rol, rows):
    if n_clicks > 0 and name and password and email and rol:
        new_row = {"nombre": name, "email": email, "rol": rol}
        rows.append(new_row)
        db_handler = current_app.config["sqlite_handler"]
        db_handler.insert(
            "user_info", {"usuario": name, "psw": password, "email": email, "role": rol}
        )
    return rows


@callback(
    Output("output-users", "children"),
    Input("usuarios-table", "data_previous"),
    Input("usuarios-table", "data"),
)
def update_or_delete_users(previous_rows, current_rows):
    if previous_rows is None:
        previous_rows = []

    previous_set = {row["nombre"]: row for row in previous_rows}
    current_set = {row["nombre"]: row for row in current_rows}

    db_handler = current_app.config["sqlite_handler"]

    # Detect deleted rows
    deleted_users = set(previous_set.keys()) - set(current_set.keys())
    for user in deleted_users:
        db_handler.delete("user_info", {"usuario": user})

    # Detect updated rows
    for user, data in current_set.items():
        if user in previous_set and data != previous_set[user]:
            db_handler.update(
                "user_info",
                {"email": data["email"], "role": data["rol"]},
                {"usuario": user},
            )

    return "Usuarios actualizados"
