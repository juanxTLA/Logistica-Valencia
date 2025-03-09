import os


class Config:
    MONGO_URL = os.getenv("MONGO_URL")
