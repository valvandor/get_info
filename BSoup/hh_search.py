import os

from bs4 import BeautifulSoup as soup
import requests

URL = 'https://hh.ru/search/vacancy'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}

params = {
    'search_field': 'name',
    'order_by': 'relevance',
    'items_on_page': '50',
    'no_magic': 'true',
    'L_save_area': 'true',
}

response = requests.get(url=URL, params=params, headers=headers)

file_path = './page.txt'
if not os.path.exists(file_path):
    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(response.text)

with open(file_path, 'r') as f:
    html = f.read()

souped_page = soup(html, 'html.parser')

main_content = souped_page.find('div', attrs={'id': "a11y-main-content"})

print()
