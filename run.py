from helpers import make_data_directory
from HH_search.search_service import HeadHunterSearchService
from HH_search.request_consts import URL, HEADERS, PARAMS
from mongo.services import MongoAccessVacanciesService
from mongo.db import client


def main():
    searched_text = input('Input searched text: ')

    make_data_directory()

    text = searched_text.strip()
    file_prefix_name = text.replace(' ', '_')

    search_object = HeadHunterSearchService(URL, HEADERS, PARAMS)
    vacancies_service = MongoAccessVacanciesService(client)

    vacancies_list = search_object.make_fully_hh_search(text)

    if vacancies_list:
        vacancies_collection = vacancies_service.use_collection(f'{file_prefix_name}_vacancies')
        vacancies_service.insert(vacancies_list, vacancies_collection)


if __name__ == '__main__':
    main()
