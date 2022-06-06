from bs4 import BeautifulSoup as Soup
from typing import List

from search_services import BaseSearch
from search_services.hh.soup_parsing import HeadHunterParseMixin
from search_services.storing_files import StoringFilesService


class BaseSoupedSearch(BaseSearch, StoringFilesService):
    """
    Base class for searching via BeautifulSoup
    """

    def get_souped_page(self, request_data: dict, file_path: str) -> Soup or None:
        """
        Makes BeautifulSoup object on html code

        Params:
            file_path — path to file, which should be loaded or where to save
            request_data — dict with data for requesting with keys url, headers and params

        Returns:
            None if no html code else BeautifulSoup object
        """
        html = self.get_html_code(request_data, file_path)
        if html is not None:
            return Soup(html, 'html.parser')


class HeadHunterSearchService(HeadHunterParseMixin, BaseSoupedSearch):
    """
    This service exclusively for headhunter
    """
    def __init__(self, url, headers, params):
        super().__init__()
        self.__request_data = {
            'url': url,
            'params': params,
            'headers': headers,
        }

    def make_fully_hh_search(self, searched_text: str, folder_name: str = 'pages') -> List[dict] or None:
        """
        Parse and store data in json files with buffering

        Params:
            searched_text — searched text, which should be in vacancies names
            folder_name — suffix for directory name, default pages
        Returns:
            list with vacancies
        """
        print('Parsing and storing', end='')
        self.__request_data['params']['text'] = searched_text

        self.make_data_directory()
        dir_with_pages = self.make_cache_dir(searched_text, folder_name)
        vacancies = []
        i = 0
        while True:
            if i != 0:
                self.__request_data['params']['page'] = str(i)

            file_path = f'{dir_with_pages}page_{i + 1}.txt'
            souped_page = self.get_souped_page(self.__request_data, file_path)
            if not souped_page:
                break

            vacancies += self._get_vacancies_on_page(souped_page)
            if not self._has_next_page(souped_page):
                print()
                break
            i += 1
            print('.', end='')

        if not vacancies:
            self.remove_cache_dir(searched_text, folder_name)
            print(f'There are no vacancies for the searched text "{searched_text}"')
            return

        self.create_json_file(vacancies, searched_text.replace(' ', '_'))
        self.update_last_searched_text(searched_text)

        return vacancies
