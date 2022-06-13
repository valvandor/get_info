from typing import List
from uuid import uuid4

from lxml.html import HtmlElement

import const


class SuperJobParseMixin:
    @staticmethod
    def has_next_page(lxml_page: HtmlElement) -> bool:
        """
        Checks if the current page is the latest
        """

        next_page_element = lxml_page.xpath("//a[contains(@class, 'f-test-button-dalshe')]")
        return next_page_element != []

    def get_vacancies_on_page(self, lxml_page: HtmlElement) -> List[dict]:
        """
        Parses vacancies on page to separate containers

        Params: souped_page — parsing page

        Returns:
            list with described vacancies
        """
        vacancies = lxml_page.xpath("//div[contains(@class, 'f-test-vacancy-item')]")
        return [self.__parse_hh_vacancy(vacancy) for vacancy in vacancies]

    def __parse_hh_vacancy(self, vacancy: HtmlElement) -> dict:
        """
        Parses values for selected fields: vacancy name, link, city, min/max salary and currency

        Args:
            vacancy: HtmlElement object represented vacancy container

        Returns:
            described vacancy
        """

        vacancy_name = ''.join(vacancy.xpath(".//a[contains(@target, '_blank')][1]/text()"))
        link_value = self.base_url + ''.join(vacancy.xpath(".//a[contains(@target, '_blank')][1]/@href"))
        city = ''.join(vacancy.xpath(".//span[contains(@class, 'f-test-text-company-item-location')]/text()[1]"))
        salary_values = vacancy.xpath(".//span[contains(@class, 'f-test-text-company-item-salary')]/descendant::text()")
        min_salary, max_salary, currency = self.__get_cash_values(salary_values)
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
    def __get_cash_values(salary_values: List[str]):
        min_salary, max_salary, currency = None, None, None

        if salary_values[0] == 'от':
            value = salary_values[2]
            salary_list = value.split('\xa0')
            currency = salary_list.pop(-1).replace('.', '')
            min_salary = int(''.join(salary_list))
            max_salary = None
            return min_salary, max_salary, currency

        if salary_values[0] == 'до':
            value = salary_values[2]
            salary_list = value.split('\xa0')
            currency = salary_list.pop(-1).replace('.', '')
            max_salary = int(''.join(salary_list))
            min_salary = None

        if len(salary_values) == 9:
            salary_list = ''.join(salary_values).split('\xa0')
            currency = salary_list.pop(-1).split('/')[0].replace('.', '')
            salaries = ''.join(salary_list).split('—')
            min_salary = int(salaries[0])
            max_salary = int(salaries[1])

        return min_salary, max_salary, currency

