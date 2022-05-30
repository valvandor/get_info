from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

client = MongoClient('mongodb://localhost:27017/')


def use_collection(collection_name: str, database: Database):
    """
    Makes collection in selected database if it's not exist and select it
    """
    return Collection(database, collection_name)
