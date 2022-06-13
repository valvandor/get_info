import requests
from requests import ConnectionError, RequestException

from search_services.storing_files import StoringFilesMixin


class BaseSearch(StoringFilesMixin):
    """
    Base class for searching
    """
    def __init__(self, url, headers, params):
        super().__init__()
        self._request_data = {
            'url': url,
            'params': params,
            'headers': headers,
        }

    @staticmethod
    def __get_response(request_data) -> str or None:
        """
        Makes request to the URL using headers and params

        Params:
            request_data — dict with data for request
        Returns:
            response from URL
        Raises:
            ConnectionError: if no connection to internet
        """

        try:
            response = requests.get(**request_data)
            return response
        except ConnectionError as e:
            print(f'\nSomething with connection to internet\n> {e}\n')
            return
        except RequestException as e:
            print(f'\nSomething went wrong\n> {e}\n')
            return

    def _get_html_code(self, request_data: dict) -> str or None:
        """
        Makes request and returns html code

        Params:
            request_data — dict with data for requesting with keys url, headers and params

        Returns:
            None if no response or status code 404 else html code
        """
        response = self.__get_response(request_data)
        if not response:
            return
        if not response.status_code:
            print('\nPage not found')
            return
        if response.ok:
            return response.text
