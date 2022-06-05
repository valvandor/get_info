"""
This module provide for Vacancy object model
"""
from typing import List

from pymongo.errors import DuplicateKeyError

import const
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

    def update_many_by_field(self, data: List[dict], search_key: str) -> List[int] or None:
        """
        Updates vacancies by search_key if possible

        Args:
            data: data to be updated
            search_key: the field on which to update

        Returns:
            list of indexes which was updated in data or None if there're not updated items
            """
        print('Trying to update')
        updated_indexes = []
        for i, item in enumerate(data):
            is_update = self._update_by_field(item, search_key)
            if is_update:
                updated_indexes.append(i)
        if updated_indexes:
            return updated_indexes

    def get_objects_by_filter(self, value, filters: list):
        if 'over' in filters:
            vacancies_with_min_salary = [vacancy for vacancy in self._get_many_by_gte_filter(const.MIN_SALARY, value)]
            vacancies_with_max_salary = [vacancy for vacancy in self._get_many_by_lte_filter(const.MAX_SALARY, value)]
            for vacancy in vacancies_with_max_salary:
                if vacancy not in vacancies_with_min_salary:
                    vacancies_with_min_salary.append(vacancy)
            return vacancies_with_min_salary


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
