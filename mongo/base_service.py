from mongo.db import client


class MongoAccessDefaultService:
    """
    Base service for Access Mongo
    """
    def __init__(self, collection_name):
        self._client = client
        self._db = self._client['vacancies_searching']
        self._collection = self._db[collection_name]

    def get_db_name(self):
        return self._db.name

    def get_collection(self):
        return self._collection
