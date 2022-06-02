from mongo.db import client


class DAODefaultObject:
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

    def use_index(self, field: str):
        """
        Add index, if it's not already exist

        Args:
            field: index name
        """
        if field not in self._list_index():
            self._collection.create_index(field, unique=True)
        else:
            print(f'Index {field} already exist')

    def _list_index(self):
        return [index['key'][0][0] for index in self._collection.index_information().values()]
