import json
import os
import shutil

import const


def make_data_directory():
    """
    Makes directory for storing parsed json files
    """
    if not os.path.exists(f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}'):
        os.mkdir(f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}')


def make_cache_dir(keyword, folder_name):
    """
    Makes directories for storing loaded pages
    """
    if not os.path.exists(f'{const.ROOT_DIRECTORY}{const.CACHE_DIR_NAME}'):
        os.mkdir(f'{const.ROOT_DIRECTORY}{const.CACHE_DIR_NAME}')
    dir_with_pages = f'{const.ROOT_DIRECTORY}{const.CACHE_DIR_NAME}"{keyword}" {folder_name}/'
    if not os.path.exists(dir_with_pages):
        os.mkdir(dir_with_pages)
    return dir_with_pages


def remove_cache_dir(keyword: str, folder_name='pages'):
    """
    Remove directories with storing loaded pages
    """
    dir_with_pages = f'{const.ROOT_DIRECTORY}{const.CACHE_DIR_NAME}"{keyword}" {folder_name}/'
    if os.path.exists(dir_with_pages):
        shutil.rmtree(dir_with_pages, ignore_errors=True)


def get_searched_word():
    try:
        with open(f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{const.FILE_LAST_SEARCHED_TEXT}', 'r') as file:
            data = (json.load(file))
            search_text = data[const.SEARCHED_TEXT]
    except OSError:
        return
    return search_text
