from pymongo.errors import DuplicateKeyError

import const
from mongo.db import client


class DAODefaultObject:
    """
    Abstract data access object
    """
    def __init__(self, collection_name):
        self._client = client
        self._db = self._client['vacancies_searching']
        self._collection = self._db[collection_name]
        self.collection_name = collection_name

    def get_db_name(self):
        return self._db.name

    def get_collection(self):
        return self._collection

    def use_index(self, field: str, unique: bool = False):
        """
        Add index, if it's not already exist

        Args:
            field: index name
            unique: make field unique
        """
        if field not in self._list_index():
            self._collection.create_index(field, unique=unique)
        else:
            print(f'Index {field} already exist')

    def _list_index(self):
        return [index['key'][0][0] for index in self._collection.index_information().values()]

    @staticmethod
    def __remove_id_from_object(object):
        if object.get(const.ID):
            del object[const.ID]

    def get_object(self, key: str, value) -> dict:
        return self._collection.find_one({key: value})

    def _update_by_field(self, obj, key, upsert=False):
        value = obj[key]
        exist = self.get_object(key, value)
        if exist:
            self.__remove_id_from_object(exist)
        self.__remove_id_from_object(obj)
        if obj == exist:
            return False
        self._collection.replace_one({key: obj[key]}, obj, upsert=upsert)
        return True

    def _get_many_by_gt_filter(self, field, value):
        return self._collection.find({field: {'$gt': value}})

    def is_exist(self):
        return self.collection_name in self._db.list_collection_names()

    def is_empty(self):
        any_object = self._collection.find_one({})
        return any_object is None

    def drop(self):
        if self.is_empty:
            self._collection.drop()
            print(f'Drop empty collection {self.collection_name}')
