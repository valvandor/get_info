import os

import requests
from requests import ConnectionError


class BaseSearch:
    """
    Base class for searching
    """
    @staticmethod
    def _get_response(request_data) -> str or None:
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
        except ConnectionError as e:
            print(f'\nSomething with connection to internet \n> {e}')
            return
        return response

    def get_html_code(self, request_data: dict, file_path: str) -> str or None:
        """
        Makes request if no storing file by current url and store it.
        After that, reads data from storing file and makes it into souped page

        Params:
            file_path — path to file, which should be loaded or where to save
            request_data — dict with data for requesting with keys url, headers and params

        Returns:
            None if no response or status code 404 else html code
        """
        if not os.path.exists(file_path):
            response = self._get_response(request_data)
            if response is None:
                return
            if not response.status_code:
                os.remove(file_path)
                self._alert_not_found()
                return
            if response.ok:
                with open(file_path, 'w', encoding='UTF-8') as f:
                    f.write(response.text)
            else:
                raise Exception("that's not ok, check it out")

        with open(file_path, 'r') as f:
            page = f.read()
        return page

    @staticmethod
    def _alert_not_found():
        print('\nPage not found')
