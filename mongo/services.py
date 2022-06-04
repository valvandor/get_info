"""
This module provide for Vacancy object model
"""
from typing import List

from pymongo.errors import DuplicateKeyError

from mongo.base import DAODefaultObject


class DAOVacancies(DAODefaultObject):
    """
    Data access object for manipulate with collections stored vacancies
    """
    def __init__(self, collection_name):
        super().__init__(collection_name)
        self.db_name = self.get_db_name()
        self.collection_name = collection_name
        self.collection = self.get_collection()

    def insert_many(self, data: list) -> True or List[int]:
        """
        Add vacancies to collection

        Args:
            data: inserted vacancies with at least one item, which should be like: {
                '_id': 'id',
                'vacancy_name': 'some vacancy name',
                'link': 'correct link',
                'city': 'any city',
                'min_salary': 'lower salary limit',
                'max_salary': 'upper salary limit',
                'currency': 'currency'
            }
        Returns:
            if success True, else list with indexes of repeated vacancies
        Raises:
            DuplicateKeyError: if repeated id or another index
        """
        print(f'Loading data to database {self.db_name} in collection {self.collection_name}', end='')
        repeated_index_list = []
        for i, vacancy in enumerate(data):
            try:
                self.collection.insert_one(vacancy)
                if not i % 100:
                    print('.', end='')
            except DuplicateKeyError:
                repeated_index_list.append(i)
        print()
        return repeated_index_list if repeated_index_list else False

    def update_many_by_field(self, data: List[dict], search_key: str):
        """
        Updates vacancies by
        """
        print('Trying to update')
        for item in data:
            is_update = self._update_by_field(item, search_key)
            if is_update:
                print(f'Successful update vacancy {item[search_key]}')


class DAOSearchedText(DAODefaultObject):
    """
    Data access object for manipulate with collection stored searched texts
    """
    def __init__(self, collection_name):
        super().__init__(collection_name)
        self.db_name = self.get_db_name()
        self.collection_name = collection_name
        self.collection = self.get_collection()

    def insert(self, item: dict) -> bool:
        """
        Insert into collection new searched text

        Args:
            item: searched text, should be like: {
                'searched_text': 'something'
            }

        Returns:
            True or False depending on successful insertion
        """
        print(f'Loading data to database {self.db_name} in collection {self.collection_name}')
        try:
            self.collection.insert_one(item)
            return True
        except DuplicateKeyError as e:
            print(f"Repeated searched text: {e.details.get('keyValue')}")
            return False
