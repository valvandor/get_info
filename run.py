import const
from HH_search.search_service import HeadHunterSearchService
from HH_search.request_consts import URL, HEADERS, PARAMS
from mongo.services import MongoAccessVacanciesService, MongoAccessSearchedTextService


def main():
    searched_text = input('Input searched text: ')

    text = searched_text.strip()
    file_prefix_name = text.replace(' ', '_')

    search_object = HeadHunterSearchService(URL, HEADERS, PARAMS)

    vacancies_list = search_object.make_fully_hh_search(text)
    searched_text = search_object.get_last_searched_text()

    if vacancies_list:
        searched_text_collection = MongoAccessSearchedTextService(const.SEARCHED_COLLECTION)
        searched_text_collection.use_index(const.SEARCHED_TEXT_KEY)
        searched_text_collection.insert(searched_text)

        vacancies_collection = MongoAccessVacanciesService(f'collection_{file_prefix_name}_vacancies')
        vacancies_collection.insert_vacancies(vacancies_list)
        vacancies_collection.use_index('link')



if __name__ == '__main__':
    main()
