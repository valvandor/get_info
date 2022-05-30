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


def remove_cache_dir(prefix: str, folder_name: str):
    """
    Remove directories with storing loaded pages
    """
    dir_with_pages = f'{const.ROOT_DIRECTORY}{const.CACHE_DIR_NAME}"{prefix}" {folder_name}/'
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


def write_to_json_file(data, file_path: str):
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