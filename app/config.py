import os


class Config:
    MONGO_URL = os.getenv("MONGO_URL")
    SQLITE_URL = os.path.join(os.path.dirname(__file__), "db", "users_sqlite.db")
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
