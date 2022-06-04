from uuid import uuid4

from bs4 import BeautifulSoup as Soup
from typing import List

import const


class HeadHunterParseMixin:
    """
    This class provides handy methods for HeadHunter Service
    """

    @staticmethod
    def _has_next_page(souped_page: Soup) -> bool:
        """
        Checks if the current page is the latest
        """
        return not souped_page.find('a', attrs={'data-qa': 'pager-next'}) is None

    def _get_vacancies_on_page(self, souped_page: Soup) -> List[dict]:
        """
        Parses vacancies on page to separate containers

        Params: souped_page — parsing page

        Returns:
            list with described vacancies
        """
        main_content = souped_page.find('div', attrs={'id': "a11y-main-content"})
        try:
            vacancies_anchors = main_content.findAll('div', {'class': ['vacancy-serp-item-body__main-info']})
            return [self.__parse_hh_vacancy(anchor) for anchor in vacancies_anchors]
        except AttributeError:
            return

    def __parse_hh_vacancy(self, anchor: Soup) -> dict:
        """
        Parses values for selected fields: vacancy name, link, city, min/max salary and currency
        Params:
            anchor — souped object represented vacancies container
        Raise:
            TypeError if city is not define
        Returns:
            list with described vacancy
        """
        link_anchor = anchor.find('a', attrs={'class': ['bloko-link']})
        link_value = link_anchor['href']
        vacancy_name = link_anchor.text

        cash_info = anchor.find('span', attrs={'class': ['bloko-header-section-3']})
        if cash_info is None:
            min_salary, max_salary, currency = None, None, None
        else:
            min_salary, max_salary, currency = self.__get_cash_values(cash_info.text)

        try:
            city = anchor.find('div', attrs={'data-qa': "vacancy-serp__vacancy-address"}).text
        except TypeError:
            city = None

        return {
            const.ID: str(uuid4()),
            const.VACANCY_NAME: vacancy_name,
            const.LINK: link_value,
            const.CITY: city,
            const.MIN_SALARY: min_salary,
            const.MAX_SALARY: max_salary,
            const.CURRENCY: currency,
        }

    @staticmethod
    def __get_cash_values(raw_data) -> tuple:
        """
        Parse input string to tuple with 3 elements.
        If some of this elements is not exist, define as None

        Params:
            input_string — string like '100 - 10000 RUB' or something like that

        Returns:
            tuple of min salary, max salary and kind of currency; None for each if empty
        """
        raw_data = raw_data.replace('<!-- -->', '')
        max_salary = None
        min_salary = None
        currency = None

        sep_position = raw_data.find('–')
        if sep_position != -1:
            min_salary = int(''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
            max_salary = int(
                ''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isdigit()]))
            sep_position = raw_data.rfind(' ')
            currency = ''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isalpha()])
            currency = currency if len(currency) > 0 else None
        else:
            sep_position = raw_data.rfind(' ')
            if sep_position != -1:
                if raw_data.find('от') != -1:
                    min_salary = int(
                        ''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
                if raw_data.find('до') != -1:
                    max_salary = int(
                        ''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
                currency = ''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isalpha()])
                currency = currency if len(currency) > 0 else None
            elif len(raw_data) > 0:
                max_salary = ''.join([raw_data[i] for i in range(0, -1, -1) if raw_data[i].isdigit()][::-1])
                max_salary = int(max_salary) if len(max_salary) > 0 else None
                min_salary = max_salary
            else:
                min_salary = max_salary = currency = None
        return min_salary, max_salary, currency
