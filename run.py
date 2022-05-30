import json

import const
from helpers import make_data_directory, remove_cache_dir
from HH_search.search_service import HeadHunterSearchService
from HH_search.request_consts import URL, HEADERS, PARAMS
from mongo.services import MongoAccessVacanciesService
from mongo.db import client


def write_to_json_file(data, file_path: str):
    """
    Writes to file via encoding utf-8

    Args:
        data: which to save, must be json-format
        file_path: where to save, must be existed

    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)


def main():
    searched_text = input('Input searched text: ')

    make_data_directory()

    text = searched_text.strip()
    file_prefix_name = text.replace(' ', '_')

    search_object = HeadHunterSearchService(URL, HEADERS, PARAMS)
    vacancies_service = MongoAccessVacanciesService(client)

    json_file_path = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{file_prefix_name}{const.FILE_EXTENSION}'
    vacancies_list = search_object.make_fully_hh_search(text)

    if not vacancies_list:
        remove_cache_dir(text)
    else:
        write_to_json_file(vacancies_list, json_file_path)
        last_searched_text_file = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{const.FILE_LAST_SEARCHED_TEXT}'
        write_to_json_file({const.SEARCHED_TEXT: text}, last_searched_text_file)

        current_collection = vacancies_service.use_collection(f'vacancies_{file_prefix_name}')
        vacancies_service.insert(vacancies_list, current_collection)


if __name__ == '__main__':
    main()
