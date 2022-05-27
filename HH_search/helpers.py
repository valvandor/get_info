import os

import requests
from requests import ConnectionError


def get_response(request_data: dict) -> str or None:
    """
    Makes request to the URL using headers and params

    Args:
        request_data: dict with data for request
    Returns -> str or None:
        response from URL
    Raises:
        ConnectionError: if not connect to internet
    """

    try:
        response = requests.get(**request_data)
    except ConnectionError as e:
        print(f'\nNo active connection to internet \n{e}')
        response = None
    return response


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


def make_cache_dir(keyword, folder_name):
    if not os.path.exists('./cache/'):
        os.mkdir('./cache/')
    dir_with_pages = f'./cache/"{keyword}" {folder_name}/'
    if not os.path.exists(dir_with_pages):
        os.mkdir(dir_with_pages)
    return dir_with_pages
