import json
import os
import shutil

import const


class StoringFilesService:
    """
    Service for storing files
    """
    def __init__(self):
        self._root_dir = const.ROOT_DIRECTORY
        self._data_dir = const.DATA_DIRECTORY
        self._cache_dir = const.CACHE_DIRECTORY
        self._json_file_suffix = const.JSON_SUFFIX_FILE
        self._searched_text_key = const.SEARCHED_TEXT_KEY
        self._file_containing_last = const.FILE_CONTAINING_LAST
        self.last_searched_text_file = f'{self._root_dir}{self._data_dir}{self._file_containing_last}'

    def _get_path_to_json_file(self, prefix):
        return f'{self._root_dir}{self._data_dir}{prefix}{self._json_file_suffix}'

    def create_json_file(self, vacancies, prefix):
        json_file_path = self._get_path_to_json_file(prefix)
        self._write_to_json_file(vacancies, json_file_path)

    def update_last_searched_text(self, searched_text):
        data = {self._searched_text_key: searched_text}
        self._write_to_json_file(data, self.last_searched_text_file)

    def make_data_directory(self):
        """
        Makes directory for storing parsed json files
        """
        cahce_dir_path = f'{self._root_dir}{self._data_dir}'
        if not os.path.exists(cahce_dir_path):
            os.mkdir(cahce_dir_path)

    def make_cache_dir(self, keyword, folder_name):
        """
        Makes directories for storing loaded pages
        """
        cache_dir_path = f'{self._root_dir}{self._cache_dir}'
        if not os.path.exists(cache_dir_path):
            os.mkdir(cache_dir_path)
        dir_with_pages = f'{cache_dir_path}"{keyword}" {folder_name}/'
        if not os.path.exists(dir_with_pages):
            os.mkdir(dir_with_pages)
        return dir_with_pages

    def remove_cache_dir(self, prefix: str, folder_name: str):
        """
        Remove directories with storing loaded pages
        """
        dir_with_pages = f'{self._root_dir}{self._cache_dir}"{prefix}" {folder_name}/'
        if os.path.exists(dir_with_pages):
            shutil.rmtree(dir_with_pages, ignore_errors=True)

    def get_last_searched_text(self) -> dict or None:
        """
        Returns last searched text
        """
        try:
            with open(self.last_searched_text_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None

    @staticmethod
    def _write_to_json_file(data, file_path: str):
        """
        Writes to file via encoding utf-8

        Args:
            data: which to save, must be json-format
            file_path: where to save, must be existed

        Returns:
            None
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)