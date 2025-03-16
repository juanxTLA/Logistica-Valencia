from pymongo import MongoClient

from .database_adapter import DatabaseAdapter


class MongoDBHandler(DatabaseAdapter):
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

    def insert(self, collection: str, data: dict):
        collection = self.db[collection]
        collection.insert(data)

    def select(self, collection: str, query: dict):
        collection = self.db[collection]
        return collection.find(query)

    def update(self, collection: str, query: dict, new_values: dict):
        collection = self.db[collection]
        collection.update_one(query, {"$set": new_values})

    def delete(self, collection: str, query: dict):
        collection = self.db[collection]
        collection.delete_one(query)

    def disconnect(self):
        self.client.close()
