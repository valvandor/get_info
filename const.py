"""
Constants for manipulate with files for storing
"""
#  should be for mongo
FILE_PATHS_CONST = {
    'root_directory': './',  # relative path from place, where search method of HH search service is called
    'data_directory': 'data/',
    'cache_directory': 'cache/',
    'json_file_suffix': '_vacancies.json',
    'key_for_last': 'searched_text',
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