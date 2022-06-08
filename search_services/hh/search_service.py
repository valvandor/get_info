import time

from bs4 import BeautifulSoup as Soup
from typing import List

from search_services import BaseSearch
from search_services.hh.soup_parsing import HeadHunterParseMixin


class BaseSoupedSearch(BaseSearch):
    """
    Base class for searching via BeautifulSoup
    """

    def _get_souped_page(self, request_data: dict) -> Soup or None:
        """
        Makes BeautifulSoup object on html code

        Params:
            request_data — dict with data for requesting with keys url, headers and params

        Returns:
            None if no html code else BeautifulSoup object
        """
        html = self._get_html_code(request_data)
        if html is not None:
            return Soup(html, 'html.parser')


class HeadHunterSearchService(HeadHunterParseMixin, BaseSoupedSearch):
    """
    This service exclusively for headhunter
    """
    def __init__(self, url, headers, params):
        super().__init__(url, headers, params)
        self.service_name = 'hh'

    def _get_vacancies(self) -> List[dict] or None:
        """
        Gets all vacancies

        Returns:
            vacancies on current page or None
        """
        vacancies = []
        i = 0
        while True:
            time.sleep(1)
            souped_page = self._get_souped_page(self._request_data)
            if not souped_page:
                break

            new_vacancies = self.get_vacancies_on_page(souped_page)
            vacancies += new_vacancies

            if not self.has_next_page(souped_page) or not new_vacancies:
                break
            i += 1
            print('.', end='')
        return vacancies

    def make_hh_searching(self, searched_text: str) -> List[dict] or None:
        """
        Parse and store data in json files with buffering

        Params:
            folder_name — suffix for directory name, default hh_pages
        Returns:
            list with vacancies or None
        """
        print('Parsing and storing from HeadHunter')
        self._request_data['params']['text'] = searched_text

        vacancies = self._get_vacancies()

        if not vacancies:
            print(f'There are no vacancies for the searched text "{searched_text}"')
            return

        self._make_json_file(vacancies, searched_text.replace(' ', '_') + '_' + self.service_name)
        self._update_last_searched_text(searched_text.strip())

        return vacancies
