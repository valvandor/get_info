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
    raw_data = raw_data.replace('<!-- -->', '')
    max_salary = None
    min_salary = None
    currency = None

    sep_position = raw_data.find('–')
    if sep_position != -1:
        min_salary = int(''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
        max_salary = int(''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isdigit()]))
        sep_position = raw_data.rfind(' ')
        currency = ''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isalpha()])
        currency = currency if len(currency) > 0 else None
    else:
        sep_position = raw_data.rfind(' ')
        if sep_position != -1:
            if raw_data.find('от') != -1:
                min_salary = int(''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
            if raw_data.find('до') != -1:
                max_salary = int(''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
            currency = ''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isalpha()])
            currency = currency if len(currency) > 0 else None
        elif len(raw_data) > 0:
            max_salary = ''.join([raw_data[i] for i in range(0, -1, -1) if raw_data[i].isdigit()][::-1])
            max_salary = int(max_salary) if len(max_salary) > 0 else None
            min_salary = max_salary
        else:
            min_salary = max_salary = currency = None
    return min_salary, max_salary, currency


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

pprint(vacancies)
