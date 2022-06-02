from HH_search.search_service import HeadHunterSearchService
from HH_search.request_consts import URL, HEADERS, PARAMS
from mongo.services import MongoAccessVacanciesService


def main():
    searched_text = input('Input searched text: ')

    text = searched_text.strip()
    file_prefix_name = text.replace(' ', '_')

    search_object = HeadHunterSearchService(URL, HEADERS, PARAMS)

    vacancies_list = search_object.make_fully_hh_search(text)

    if vacancies_list:
        vacancies_collection = MongoAccessVacanciesService(f'collection_{file_prefix_name}_vacancies')
        vacancies_collection.insert_vacancies(vacancies_list)


if __name__ == '__main__':
    main()
