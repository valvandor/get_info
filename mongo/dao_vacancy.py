"""
This module provide for Vacancy object model
"""
import uuid

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


class DAOVacancy:
    """
    Vacancy data access object
    """
    def __init__(self, collection: Collection):
        self.vacancies_collection = collection

    def insert(self, data: list):
        """
        Add vacancies to collection

        Args:
            data: inserted data with at least one item
        Returns:
            None
        Raises:
            DuplicateKeyError: if repeated id
        """
        for i, vacancy in enumerate(data):
            try:
                self.vacancies_collection.insert_one(vacancy)
            except DuplicateKeyError:
                print('There was a problem with {} with index {} of inserted_list'.format(vacancy, i))
