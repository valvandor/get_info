import os

import requests
from bs4 import BeautifulSoup as Soup

from HH_search.helpers import make_cache_dir
from HH_search.mixin import ParseMixin


class BaseSearch:

    @staticmethod
    def _get_response(request_data) -> str or None:
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

    """

    def __init__(self, url, headers, params):
        self.url = url,
        self.headers = headers,
        self.params = params
        self._request_data = {
            'url': url,
            'params': params,
            'headers': headers,
        }

    def make_fully_hh_search(self, search_word, folder_name='pages') -> list:
        dir_with_pages = make_cache_dir(search_word, folder_name)

        self.params['text'] = search_word
        vacancies = []
        i = 0
        while True:
            file_path = f'./{dir_with_pages}/page_{i + 1}.txt'
            if i != 0:
                self.params['page'] = str(i)

            if not os.path.exists(file_path):
                response = self._get_response(self._request_data)
                if response.status_code == 404:
                    os.remove(f'./{dir_with_pages}/page_{i + 1}.txt')
                    break
                with open(file_path, 'w', encoding='UTF-8') as f:
                    f.write(response.text)

            with open(file_path, 'r') as f:
                html = f.read()
            souped_page = Soup(html, 'html.parser')

            main_content = souped_page.find('div', attrs={'id': "a11y-main-content"})
            vacancy_anchors = main_content.findAll('div', {'class': ['vacancy-serp-item-body__main-info']})
            vacancies_on_page = self.parse_hh_vacancy(vacancy_anchors)
            vacancies += vacancies_on_page

            if souped_page.find('a', attrs={'data-qa': 'pager-next'}) is None:
                break
            i += 1
            print('.', end='')
        return vacancies
