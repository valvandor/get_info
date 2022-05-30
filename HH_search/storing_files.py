import json
import os
import shutil

from const import FILE_PATHS_CONST


class StoringFilesService:
    """
    Service for storing files
    """
    def __init__(self):
        self._root_dir = FILE_PATHS_CONST['root_directory']
        self._data_dir = FILE_PATHS_CONST['data_directory']
        self._cache_dir = FILE_PATHS_CONST['cache_directory']
        self._json_file_suffix = FILE_PATHS_CONST['json_file_suffix']
        self._key_for_last = FILE_PATHS_CONST['key_for_last']
        self._file_containing_last = FILE_PATHS_CONST['file_containing_last']

    def get_path_to_json_file(self, prefix):
        return f'{self._root_dir}{self._data_dir}{prefix}{self._json_file_suffix}'

    def get_path_to_file_containing_last(self):
        return f'{self._root_dir}{self._data_dir}{self._file_containing_last}'

    def create_json_file(self, vacancies, prefix):
        json_file_path = self.get_path_to_json_file(prefix)
        self._write_to_json_file(vacancies, json_file_path)

    def update_last_searched_text(self, searched_text):
        last_searched_text_file = self.get_path_to_file_containing_last()
        self._write_to_json_file({self._key_for_last: searched_text}, last_searched_text_file)

    def make_data_directory(self):
        """
        Makes directory for storing parsed json files
        """
        if not os.path.exists(f'{self._root_dir}{self._data_dir}'):
            os.mkdir(f'{self._root_dir}{self._data_dir}')

    def make_cache_dir(self, keyword, folder_name):
        """
        Makes directories for storing loaded pages
        """
        if not os.path.exists(f'{self._root_dir}{self._cache_dir}'):
            os.mkdir(f'{self._root_dir}{self._cache_dir}')
        dir_with_pages = f'{self._root_dir}{self._cache_dir}"{keyword}" {folder_name}/'
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

    def get_last_searched_text(self):
        try:
            with open(f'{self._root_dir}{self._data_dir}{self._file_containing_last}', 'r') as file:
                data = (json.load(file))
                search_text = data[self.__searched_text]
        except OSError:
            return
        return search_text

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
