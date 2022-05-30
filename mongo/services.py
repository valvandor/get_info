"""
This module provide for Vacancy object model
"""
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError


class MongoAccessVacanciesService:
    """
    This service is exclusive for vacancies_searching database
    """
    def __init__(self, client):
        self.client = client
        self.vacancy_db = client['vacancies_searching']
        self.collection_name = None

    def use_collection(self, collection_name: str) -> Collection:
        """
        Makes and uses collection if it's not exist or select it
        """
        self.collection_name = collection_name
        return Collection(self.vacancy_db, collection_name)

    def insert(self, data: list, collection: Collection):
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
            collection: selected collection
        Returns:
            None
        Raises:
            DuplicateKeyError: if repeated id
            ServerSelectionTimeoutError: if no active client
        """
        print(f'Loading data to database {self.vacancy_db.name} in collection {self.collection_name}', end='')
        for i, vacancy in enumerate(data):
            try:
                collection.insert_one(vacancy)
                if not i % 20:
                    print('.', end='')
            except DuplicateKeyError:
                print('\nThere was a problem at index {} of inserted list with {}'.format(i, vacancy), end='')
            except ServerSelectionTimeoutError:
                print('\nCheck your mongo client')
                break
