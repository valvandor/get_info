import os
import uuid

from bs4 import BeautifulSoup as Soup

from hh_consts import request_data
from helpers import get_response, get_cash_values


def parse_hh_vacancy(anchors):
    vacancies = []

    for content in anchors:
        link_anchor = content.find('a', attrs={'class': ['bloko-link']})
        link_value = link_anchor['href']
        vacancy_name = link_anchor.text

        cash_info = content.find('span', attrs={'class': ['bloko-header-section-3']})
        if cash_info is None:
            min_salary, max_salary, currency = None, None, None
        else:
            min_salary, max_salary, currency = get_cash_values(cash_info.text)

        try:
            city = content.find('div', attrs={'data-qa': "vacancy-serp__vacancy-address"}).text
        except TypeError:
            city = None

        vacancies.append({
            'id_': str(uuid.uuid4()),
            'vacancy_name': vacancy_name,
            'link': link_value,
            'city': city,
            'min_salary': min_salary,
            'max_salary': max_salary,
            'currency': currency,
        })

    return vacancies


def make_fully_hh_search_by_word(keyword, folder_name='pages') -> list:
    if not os.path.exists(f'./{folder_name}/'):
        os.mkdir(f'./{folder_name}/')
    request_data['params']['page'] = keyword
    vacancies = []
    i = 0
    while True:
        file_path = f'./{folder_name}/page_{i + 1}.txt'
        if i != 0:
            request_data['params']['page'] = str(i)

        if not os.path.exists(file_path):
            response = get_response(request_data)
            if response.status_code == 404:
                os.remove(f'./{folder_name}/page_{i + 1}.txt')
                break
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(response.text)

        with open(file_path, 'r') as f:
            html = f.read()
        souped_page = Soup(html, 'html.parser')

        main_content = souped_page.find('div', attrs={'id': "a11y-main-content"})
        vacancy_anchors = main_content.findAll('div', {'class': ['vacancy-serp-item-body__main-info']})
        vacancies_on_page = parse_hh_vacancy(vacancy_anchors)
        vacancies += vacancies_on_page

        if souped_page.find('a', attrs={'data-qa': 'pager-next'}) is None:
            break
        i += 1
    return vacancies

