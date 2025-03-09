import os
import sqlite3

from flask import session

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
            f"INSERT INTO {collection} (usuario, password, rol, email) VALUES (?, ?, ?, ?)",
            (data["usuario"], data["password"], data["rol"], data["email"]),
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
            f"UPDATE {collection} SET password = ?, rol = ?, email = ? WHERE usuario = ?",
            (data["password"], data["rol"], data["email"], condition["usuario"]),
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
        cursor.execute(
            "SELECT * FROM user_info WHERE usuario = ? AND psw = ?", (username, psw)
        )
        user = cursor.fetchone()
        connection.close()
        if user:
            session["logged_in_user"] = username
            return True
        return False
