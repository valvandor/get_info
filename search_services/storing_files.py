import json
import os

from search_services import storing_const as const


class StoringFilesMixin:
    """
    Class represent methods for storing files
    """

    @staticmethod
    def _make_json_file(data, prefix: str):
        """
        Writes to file via encoding utf-8

        Args:
            data: which to save, must be json-format
            prefix: prefix for json file name
        """
        cache_dir = f'{const.ROOT_DIR}{const.DATA_DIR}'
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        json_file_path = f'{cache_dir}{prefix}_vacancies.json'
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    @staticmethod
    def _update_last_searched_text(searched_text):
        """

        """
        data = {const.SEARCHED_TEXT_KEY: searched_text}
        path = f'{const.ROOT_DIR}{const.FILE_CONTAINING_LAST}'
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    @staticmethod
    def get_last_searched_text() -> dict or None:
        """
        Returns last searched text
        """
        try:
            with open(f'{const.ROOT_DIR}{const.FILE_CONTAINING_LAST}', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None
