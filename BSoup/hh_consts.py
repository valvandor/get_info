URL = 'https://hh.ru/search/vacancy'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}

params = {
    'search_field': 'name',
    'order_by': 'relevance',
    'items_on_page': '20',
    'no_magic': 'true',
    'L_save_area': 'true',
}

request_data = {
    'url': URL,
    'params': params,
    'headers': headers,
}
