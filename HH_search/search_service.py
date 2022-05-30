import os

import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as Soup
from typing import List

import const
from helpers import make_cache_dir, remove_cache_dir, write_to_json_file
from HH_search.mixin import HeadHunterParseMixin


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
            print(f'\nNo active connection to internet \n{e}')
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
            None if response status code 404 else BeautifulSoup object
        """
        if not os.path.exists(file_path):
            response = self.get_response(request_data)
            if not response.status_code:
                os.remove(file_path)
                self._alert_not_found()
                return
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(response.text)

        with open(file_path, 'r') as f:
            html = f.read()
        return Soup(html, 'html.parser')


class HeadHunterSearchService(HeadHunterParseMixin, BaseSearch):
    """
    This class exclusively for headhunter
    """

    def __init__(self, url, headers, params):
        self.__url = url,
        self.__headers = headers,
        self._params = params
        self.__request_data = {
            'url': url,
            'params': params,
            'headers': headers,
        }
        self.__searched_text = None
        self.__json_file_prefix = None

    @staticmethod
    def _alert_starting_searching():
        print('Parsing and storing', end='')

    def make_fully_hh_search(self, searched_text: str, folder_name: str = 'pages') -> List[dict] or None:
        """
        Parse and store data in json files with buffering

        Params:
            searched_text — searched text, which should be in vacancies names
            folder_name — suffix for directory name, default pages
        Returns:
            list with vacancies
        """
        self.__searched_text = searched_text
        self.__json_file_prefix = searched_text.replace(' ', '_')
        self._alert_starting_searching()
        self._params['text'] = searched_text

        dir_with_pages = make_cache_dir(searched_text, folder_name)
        vacancies = []
        i = 0
        while True:
            if i != 0:
                self.__request_data['params']['page'] = str(i)

            file_path = f'./{dir_with_pages}/page_{i + 1}.txt'
            souped_page = self._get_souped_page(self.__request_data, file_path)
            if not souped_page:
                break

            vacancies += self._get_vacancies_on_page(souped_page)

            if souped_page.find('a', attrs={'data-qa': 'pager-next'}) is None:
                print()
                break
            i += 1
            self.__imitate_loading()

        if not vacancies:
            remove_cache_dir(self.__searched_text, folder_name)
            self._alert_nothing_found()
            return

        json_file_path = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{self.__json_file_prefix}{const.FILE_EXTENSION}'
        write_to_json_file(vacancies, json_file_path)

        last_searched_text_file = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{const.FILE_LAST_SEARCHED_TEXT}'
        write_to_json_file({const.SEARCHED_TEXT: searched_text}, last_searched_text_file)
        return vacancies

    def _alert_nothing_found(self):
        print(f'There are no vacancies for the searched text "{self.__searched_text}"')

    @staticmethod
    def __imitate_loading():
        print('.', end='')
