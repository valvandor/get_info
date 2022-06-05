import os

import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as Soup
from typing import List

from search_services.hh.parsing import HeadHunterParseMixin
from search_services.hh.storing_files import StoringFilesService


class BaseSearch:
    """
    Base class for searching
    """
    @staticmethod
    def get_response(request_data) -> str or None:
        """
        Makes request to the URL using headers and params

        Params:
            request_data — dict with data for request
        Returns:
            response from URL
        Raises:
            ConnectionError: if no connection to internet
        """

        try:
            response = requests.get(**request_data)
        except ConnectionError as e:
            print(f'\nSomething with connection to internet \n> {e}')
            return
        return response

    @staticmethod
    def _alert_not_found():
        print('\nPage not found')

    def _get_souped_page(self, request_data: dict, file_path: str) -> Soup or None:
        """
        Makes request if no storing file by current url and store it.
        After that, reads data from storing file and makes it into souped page

        Params:
            file_path — path to file, which should be loaded or where to save
            request_data — dict with data for requesting with keys url, headers and params

        Returns:
            None if no response or status code 404 else BeautifulSoup object
        """
        if not os.path.exists(file_path):
            response = self.get_response(request_data)
            if response is None:
                return
            if not response.status_code:
                os.remove(file_path)
                self._alert_not_found()
                return
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(response.text)

        try:
            with open(file_path, 'r') as f:
                html = f.read()
        except FileNotFoundError:
            print(f"There's no file {file_path}")
            return None
        return Soup(html, 'html.parser')


class HeadHunterSearchService(HeadHunterParseMixin, StoringFilesService, BaseSearch):
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
            souped_page = self._get_souped_page(self.__request_data, file_path)
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

