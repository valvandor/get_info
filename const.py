"""
Constants for manipulate with files for storing
"""

DB_NAME = 'vacancies_searching'
SEARCHED_COLLECTION = 'collection_searched_text'
SEARCHED_TEXT_KEY = 'searched_text'

FILE_PATHS_CONST = {
    'root_directory': './',  # relative path from place, where search method of HH search service is called
    'data_directory': 'data/',
    'cache_directory': 'cache/',
    'json_file_suffix': '_vacancies.json',
    'searched_text_key': SEARCHED_TEXT_KEY,
    'file_containing_last': 'last_searched_text.json',
}

STORING_CONST = {
    'id': '_id',
    'vacancy_name': 'vacancy_name',
    'link': 'link',
    'city': 'city',
    'min_salary': 'min_salary',
    'max_salary': 'max_salary',
    'currency': 'currency',
}
