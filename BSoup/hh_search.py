import json
import os

from bs4 import BeautifulSoup as Soup

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
            'vacancy_name': vacancy_name,
            'link': link_value,
            'city': city,
            'min_salary': min_salary,
            'max_salary': max_salary,
            'currency': currency,
        })

    return vacancies


URL = 'https://hh.ru/search/vacancy'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}

params = {
    'search_field': 'name',
    'order_by': 'relevance',
    'text': 'python',
    'items_on_page': '20',
    'no_magic': 'true',
    'L_save_area': 'true',
}

request_data = {
    'url': URL,
    'params': params,
    'headers': headers,
}

if not os.path.exists('./pages/'):
    os.mkdir('./pages/')

vacancies = []
i = 0

while True:
    file_path = f'./pages/page_{i + 1}.txt'
    if i != 0:
        request_data['params']['page'] = str(i)

    if not os.path.exists(file_path):
        response = get_response(request_data)
        if response.status_code == 404:
            os.remove(f'./pages/page_{i + 1}.txt')
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

with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(vacancies, file)
