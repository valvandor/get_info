import const
from HH_search.search_service import HeadHunterSearchService
from HH_search.request_consts import URL, HEADERS, PARAMS
from mongo.services import DAOVacancies, DAOSearchedText


def main():
    searched_text = input('Input searched text: ')

    text = searched_text.strip()
    file_prefix_name = text.replace(' ', '_')

    search_object = HeadHunterSearchService(URL, HEADERS, PARAMS)

    vacancies_list = search_object.make_fully_hh_search(text)
    last_searched_data = search_object.get_last_searched_text()

    vacancies_collection = DAOVacancies(f'collection_{file_prefix_name}_vacancies')  # TODO: remove if no vacancies
    repeated_vacancies = []
    if vacancies_list:
        searched_text_collection = DAOSearchedText(const.SEARCHED_COLLECTION)
        searched_text_collection.use_index(const.SEARCHED_TEXT_KEY, unique=True)
        is_new_search = searched_text_collection.insert(last_searched_data)
        if is_new_search:
            vacancies_collection.use_index(const.LINK, unique=True)
            unsuccessful_indexes = vacancies_collection.insert_many(vacancies_list)
            if unsuccessful_indexes:
                repeated_vacancies = [vacancies_list[i] for i in range(len(vacancies_list))
                                      if i in unsuccessful_indexes]
        else:
            repeated_vacancies = vacancies_list
        vacancies_collection.update_many_by_field(repeated_vacancies, const.LINK)


if __name__ == '__main__':
    main()
