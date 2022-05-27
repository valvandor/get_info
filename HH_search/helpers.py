import os

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
    if not os.path.exists(f'../{const.CACHE_DIR_NAME}'):
        os.mkdir(f'../{const.CACHE_DIR_NAME}')
    dir_with_pages = f'../{const.CACHE_DIR_NAME}"{keyword}" {folder_name}/'
    if not os.path.exists(dir_with_pages):
        os.mkdir(dir_with_pages)
    return dir_with_pages
