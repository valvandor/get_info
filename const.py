"""
Constants for manipulate with files for storing
"""

DB_NAME = 'vacancies_searching'
SEARCHED_COLLECTION = 'collection_searched_text'

ROOT_DIRECTORY = './'  # relative path from place, where search method of HH search service is called
DATA_DIRECTORY = 'data/'
CACHE_DIRECTORY = 'cache/'
JSON_SUFFIX_FILE = '_vacancies.json'
SEARCHED_TEXT_KEY = 'searched_text'
FILE_CONTAINING_LAST = 'last_searched_text.json'

STORING_CONST = {
    'id': '_id',
    'vacancy_name': 'vacancy_name',
    'link': 'link',
    'city': 'city',
    'min_salary': 'min_salary',
    'max_salary': 'max_salary',
    'currency': 'currency',
}
