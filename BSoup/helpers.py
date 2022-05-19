import requests
from requests import ConnectionError


def get_response(request_data) -> str or None:
    """
    Makes request to the URL using headers and params

    Args -> dict:
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
