import time

from bs4 import BeautifulSoup as Soup
from typing import List

from search_services import BaseSearch, request_consts
from search_services.hh.soup_parsing import HeadHunterParseMixin


class BaseSoupedSearch(BaseSearch):
    """
    Base class for searching via BeautifulSoup
    """

    def _get_souped_page(self, request_data: dict) -> Soup or None:
        """
        Makes BeautifulSoup object on html code

        Args:
            request_data: dict with data for requesting with keys url, headers and params

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
            vacancies on pages or None
        """
        vacancies = []
        i = 1
        while True:
            time.sleep(1)
            self._request_data[request_consts.PARAMS]['page'] = i
            souped_page = self._get_souped_page(self._request_data)
            if not souped_page:
                break

            vacancies += self.get_vacancies_on_page(souped_page)

            if not self.has_next_page(souped_page):
                break
            i += 1
            print('.', end='')
        return vacancies if vacancies else None

    def make_hh_searching(self, searched_text: str, buffered: bool = False) -> List[dict] or None:
        """
        Parse and store data in json files if buffered is True

        Args:
            searched_text: searched text
            buffered: neediness to save to json file, default False
        Returns:
            list with vacancies or None
        """
        print(f'Parsing{" and storing" if buffered else ""} from HeadHunter')
        self._request_data['params']['text'] = searched_text

        vacancies = self._get_vacancies()

        if vacancies is None:
            print(f'There are no vacancies for the searched text "{searched_text}"')
        else:
            if buffered:
                self._make_json_file(vacancies, searched_text.replace(' ', '_') + '_' + self.service_name)
            self._update_last_searched_text(searched_text.strip())

        return vacancies
