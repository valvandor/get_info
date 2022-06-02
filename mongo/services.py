"""
This module provide for Vacancy object model
"""
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError

import const
from mongo.base import DAODefaultObject


class DAOVacancies(DAODefaultObject):
    """
    Data access object for manipulate with collections stored vacancies
    """
    def __init__(self, collection_name):
        super().__init__(collection_name)
        self.db_name = self.get_db_name()
        self.collection = self.get_collection()

    def insert_vacancies(self, data: list):
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
            ServerSelectionTimeoutError: if no active client
        """
        print(f'Loading data to database {self.db_name}', end='')
        for i, vacancy in enumerate(data):
            try:
                self.collection.insert_one(vacancy)
                if not i % 20:
                    print('.', end='')
            except DuplicateKeyError:
                print('\nThere was a problem at index {} of inserted list with {}'.format(i, vacancy), end='')
            except ServerSelectionTimeoutError:
                print('\nCheck your mongo client')
                break


class DAOSearchedText(DAODefaultObject):
    """
    Data access object for manipulate with collection stored searched texts
    """
    def __init__(self, collection_name):
        super().__init__(collection_name)
        self.db_name = self.get_db_name()
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
        print(f'Loading data to database {self.db_name}')
        try:
            self.collection.insert_one(item)
            return True
        except DuplicateKeyError as e:
            print(f"Repeated searched text: {e.details.get('keyValue')[const.SEARCHED_TEXT_KEY]}")
            return False
