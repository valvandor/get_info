import os

import requests
from bs4 import BeautifulSoup as Soup

from HH_search.helpers import make_cache_dir
from HH_search.mixin import ParseMixin


class BaseSearch:
    """
    Base class for searching
    """
    @staticmethod
    def get_response(request_data) -> str or None:
        """
        Makes request to the URL using headers and params

        Args:
            request_data: dict with data for request
        Returns -> str or None:
            response from URL
        Raises:
            ConnectionError: if no connection to internet
        """

        try:
            response = requests.get(**request_data)
        except ConnectionError as e:
            print(f'\nNo active connection to internet \n{e}')
            response = None
        return response


class HeadHunterSearch(ParseMixin, BaseSearch):
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

    def _get_souped_page(self, file_path: str, i: int) -> Soup:
        """
        Makes request if no storing file by current url and store it.
        After that, reads data from storing file and makes it into souped page

        Args:
            file_path: path to file, which should be loaded or where to save
            i: increment, which will put to next page by param
        Returns -> BeautifulSoup object or None
        """
        if i != 0:
            self._params['page'] = str(i)

        if not os.path.exists(file_path):
            response = self.get_response(self.__request_data)
            if response.status_code == 404:
                os.remove(file_path)
                return
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(response.text)

        with open(file_path, 'r') as f:
            html = f.read()
        return Soup(html, 'html.parser')

    def make_fully_hh_search(self, search_word, folder_name='pages') -> list:
        dir_with_pages = make_cache_dir(search_word, folder_name)

        self._params['text'] = search_word
        vacancies = []
        i = 0
        while True:
            file_path = f'./{dir_with_pages}/page_{i + 1}.txt'
            souped_page = self._get_souped_page(file_path, i)
            if not souped_page:
                break

            vacancies += self._get_vacancies_on_page(souped_page)

            if souped_page.find('a', attrs={'data-qa': 'pager-next'}) is None:
                break
            i += 1

            self.__imitate_loading()
        return vacancies

    @staticmethod
    def __imitate_loading():
        print('.', end='')

