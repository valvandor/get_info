import time
from typing import List

from lxml import html
from lxml.html import HtmlElement

from search_services import BaseSearch, request_consts
from search_services.sj.xpath_parsing import SuperJobParseMixin


class BaseLxmlSearch(BaseSearch):
    """
    Base class for searching via lxml
    """

    def _get_lxml_page(self, request_data: dict) -> None or HtmlElement:
        """
        Makes HtmlElement object on html code

        Args:
            request_data: dict with data for requesting with keys url, headers and params

        Returns:
            None if no html code else HtmlElement object
        """
        html_code = self._get_html_code(request_data)
        if html_code is not None:
            return html.fromstring(html_code)


class SuperJobSearchService(SuperJobParseMixin, BaseLxmlSearch):
    """
    This service exclusively for headhunter
    """
    def __init__(self, url, headers, params):
        self.base_url = 'https://russia.superjob.ru/'
        super().__init__(url, headers, params)
        self.service_name = 'sj'

    def _get_vacancies(self) -> List[dict] or None:
        """
        Gets all vacancies

        Returns:
            vacancies on all pages or None
        """
        vacancies = []
        i = 1
        while True:
            time.sleep(1)
            self._request_data[request_consts.PARAMS]['page'] = i
            lxml_page = self._get_lxml_page(self._request_data)
            if lxml_page is None:
                break

            vacancies += self.get_vacancies_on_page(lxml_page)

            if not self.has_next_page(lxml_page):
                break
            i += 1
            print('.', end='')
        return vacancies

    def make_sj_searching(self, searched_text: str, buffered: bool = False) -> List[dict] or None:
        """
        Parse and store data in json files if buffered is True

        Args:
            searched_text: searched text
            buffered: neediness to save to json file, default False
        Returns:
            list with vacancies or None
        """
        print(f'Parsing{" and storing" if buffered else ""} from SuperJob')

        self._request_data[request_consts.PARAMS]['keywords'] = searched_text

        vacancies = self._get_vacancies()

        if not vacancies:
            print(f'There are no vacancies for the searched text "{searched_text}"')
        else:
            if buffered:
                self._make_json_file(vacancies, searched_text.replace(' ', '_') + '_' + self.service_name)
            self._update_last_searched_text(searched_text.strip())

        return vacancies
