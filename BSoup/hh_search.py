import os
from pprint import pprint

from bs4 import BeautifulSoup as Soup
from helpers import get_response


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
    'page': 0,
}

request_data = {
    'url': URL,
    'params': params,
    'headers': headers,
}


def get_cash_values(raw_data) -> tuple:
    """
    Parse input string to tuple with 3 elements.
    If some of this elements is not exist, define as None

    Args -> str:
        input_string: string like '100 - 10000 RUB' or something like that

    Returns:
        tuple of min salary, max salary and kind of currency; None for each if empty
    """
    return None, None, None


if not os.path.exists('./pages/'):
    os.mkdir('./pages/')

file_path = './pages/page.txt'

if not os.path.exists(file_path):
    response = get_response(request_data)
    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(response.text)

with open(file_path, 'r') as f:
    html = f.read()
souped_page = Soup(html, 'html.parser')

main_content = souped_page.find('div', attrs={'id': "a11y-main-content"})
vacancies = []

anchors = main_content.findAll('div', {'class': ['vacancy-serp-item-body__main-info']})
for content in anchors:
    link_anchor = content.find('a', attrs={'class': ['bloko-link']})

    link_value = link_anchor['href']
    vacancy_name = link_anchor.text

    cash_info = content.find('span', attrs={'class': ['bloko-header-section-3']})

    if cash_info is None:
        min_salary, max_salary, currency = None, None, None
    else:
        min_salary, max_salary, currency = get_cash_values(cash_info)

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

pprint(vacancies)
