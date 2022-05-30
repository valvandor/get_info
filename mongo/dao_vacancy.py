"""
This module provide for Vacancy object model
"""
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


class DAOVacancy:
    """
    This service is exclusive for Vacancies
    """
    def __init__(self, collection: Collection):
        self.vacancies_collection = collection

    def insert(self, data: list):
        """
        Add vacancies to collection

        Args:
            data: inserted data with at least one item, which should be like: {
                '_id': 'id',
                'vacancy_name': 'some vacancy name',
                'link': 'correct link',
                'city': 'any city',
                'min_salary': 'lower salary limit',
                'max_salary': 'upper salary limit',
                'currency': 'currency'
            }
        Returns:
            None
        Raises:
            DuplicateKeyError: if repeated id
        """
        for i, vacancy in enumerate(data):
            try:
                self.vacancies_collection.insert_one(vacancy)
            except DuplicateKeyError:
                print('There was a problem at index {} of inserted list with {}'.format(i, vacancy))
