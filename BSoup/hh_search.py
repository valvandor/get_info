import os

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
    'items_on_page': '50',
    'no_magic': 'true',
    'L_save_area': 'true',
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
        input_string: string like '100 - 10000 RUB'

    Returns:
        tuple of min salary, max salary and kind of currency
    """
    pass


file_path = './page.txt'

if not os.path.exists(file_path):
    response = get_response(request_data)
    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(response.text)

with open(file_path, 'r') as f:
    html = f.read()
souped_page = Soup(html, 'html.parser')
main_content = souped_page.find('div', attrs={'id': "a11y-main-content"})

link_anchor = main_content.find('a', attrs={'class': ['bloko-link']})

link_value = link_anchor['href']
vacancy_name = link_anchor.text

title_anchors = main_content.findAll('h3', attrs={'class': ['bloko-header-section-3']})
for anchor in title_anchors:
    cash_anchor = anchor.next_sibling
    if cash_anchor is None:
        print('None')
    else:
        raw_data = cash_anchor.next_sibling.text
        print(raw_data)

