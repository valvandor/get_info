from pprint import pprint

import const
from search_services.hh.search_service import HeadHunterSearchService
from search_services.request_consts import HH_REQUEST_CONST
from search_services.storing_const import SEARCHED_TEXT_KEY
from mongo.services import DAOVacancies, DAOSearchedText


def main():
    searched_text = input('Input searched text: ')

    text = searched_text.strip()
    file_prefix_name = text.replace(' ', '_')

    search_object = HeadHunterSearchService(**HH_REQUEST_CONST)

    vacancies_list = search_object.make_hh_searching(text)
    last_searched_data = search_object.get_last_searched_text()

    vacancies_collection = DAOVacancies(f'collection_{file_prefix_name}_vacancies')
    repeated_vacancies = []
    if last_searched_data and vacancies_list:
        searched_text_collection = DAOSearchedText(const.SEARCHED_TEXTS_COLLECTION)
        searched_text_collection.use_index(SEARCHED_TEXT_KEY, unique=True)
        is_new_search = searched_text_collection.insert(last_searched_data)
        if is_new_search:
            vacancies_collection.use_index(const.LINK, unique=True)
            unsuccessful_indexes = vacancies_collection.insert_many(vacancies_list)
            if unsuccessful_indexes:
                repeated_vacancies = [vacancies_list[i] for i in range(len(vacancies_list))
                                      if i in unsuccessful_indexes]
        else:
            repeated_vacancies = vacancies_list
        updated_indexes = vacancies_collection.update_many_by_field(repeated_vacancies, const.LINK)
        if updated_indexes:
            print(f'Some vacancies was updated, on indexes {updated_indexes}')
    else:
        if vacancies_collection.is_empty():
            vacancies_collection.drop()

    if vacancies_collection.is_exist():
        filters = {
            const.SALARY: 'over',
            const.CURRENCY: ['руб', 'рублей', 'rub']
        }
        vacancies_over_min = vacancies_collection.get_vacancies_over_salary(60000, filters)
        pprint(vacancies_over_min)


if __name__ == '__main__':
    main()
