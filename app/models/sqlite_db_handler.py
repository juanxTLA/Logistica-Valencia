import os
import sqlite3

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.database_adapter import DatabaseAdapter


class SQLiteDBHandler(DatabaseAdapter):
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        try:
            if not os.path.exists(self.db_path):
                connection = sqlite3.connect(self.db_path, check_same_thread=False)
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON;")
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS user_info
                                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   usuario TEXT UNIQUE NOT NULL,
                                   psw TEXT NOT NULL,
                                   email TEXT NOT NULL,
                                   role TEXT NOT NULL)"""
                )
                connection.commit()
                connection.close()
            connection = sqlite3.connect(self.db_path, check_same_thread=False)
            return connection
        except Exception as e:
            print(f"Error connecting to SQLite database: {e}")
            return None

    def insert(self, collection: str, data: dict):
        connection = self.connect()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO {collection} (usuario, psw, role, email) VALUES (?, ?, ?, ?)",
            (
                data["usuario"],
                generate_password_hash(data["psw"]),
                data["role"],
                data["email"],
            ),
        )
        connection.commit()
        connection.close()

    def select(self, collection: str, query: dict):
        connection = self.connect()
        if connection is None:
            return []
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM {collection} WHERE usuario = ?", (query["usuario"],)
        )
        result = cursor.fetchall()
        connection.close()
        return result

    def update(self, collection: str, data: dict, condition: dict):
        connection = self.connect()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute(
            f"UPDATE {collection} SET role = ?, email = ? WHERE usuario = ?",
            (data["role"], data["email"], condition["usuario"]),
        )
        connection.commit()
        connection.close()

    def delete(self, collection: str, condition: dict):
        connection = self.connect()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute(
            f"DELETE FROM {collection} WHERE usuario = ?", (condition["usuario"],)
        )
        connection.commit()
        connection.close()

    def validate_user(self, username: str, psw: str) -> bool:
        connection = self.connect()
        if connection is None:
            return False
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_info WHERE usuario = ?", (username,))
        user = cursor.fetchone()
        connection.close()
        if user and check_password_hash(user[2], psw):
            session["logged_in_user"] = username
            session["user_group"] = user[4]
            return True
        return False

    def fetch_users(self):
        connection = self.connect()
        if connection is None:
            return []
        cursor = connection.cursor()
        cursor.execute("SELECT usuario, email, role FROM user_info")
        users = cursor.fetchall()
        connection.close()
        return [{"nombre": user[0], "email": user[1], "rol": user[2]} for user in users]
