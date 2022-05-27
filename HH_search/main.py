import json
import os

from HH_search import const
from hh_search import make_fully_hh_search

searching_for = 'python'


def main(text):
    if not os.path.exists(f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}'):
        os.mkdir(f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}')

    text = text.strip()
    searched = text.replace(' ', '_')

    file_path = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{searched}{const.FILE_EXTENSION}'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(
            make_fully_hh_search(text), file)

    answer = input('\nРаспечатать количество полученных вакансий? (press Enter to deny): ')
    if answer:
        with open(file_path, 'r') as file:
            print(len(json.load(file)))


if __name__ == '__main__':
    main(searching_for)
