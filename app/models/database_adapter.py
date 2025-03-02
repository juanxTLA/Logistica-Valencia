from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):
    @abstractmethod
    def connect(self):
        """Connect to the database"""
        pass

    @abstractmethod
    def insert(self, collection: str, data: dict):
        """Insert data into the collection"""
        pass

    @abstractmethod
    def select(self, collection: str, query: dict):
        """Select data from the collection"""
        pass

    @abstractmethod
    def update(self, collection: str, data: dict, condition: dict):
        """Update data in the collection"""
        pass

    @abstractmethod
    def delete(self, collection: str, condition: dict):
        """Delete data from the collection"""
        pass

    def close(self):
        """Close connection"""
        pass
