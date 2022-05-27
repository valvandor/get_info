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

    json_file = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{searched}{const.FILE_EXTENSION}'
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(
            make_fully_hh_search(text), file)

    searched_text_file = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{const.LAST_SEARCHED_TEXT}'
    with open(searched_text_file, 'w', encoding='utf-8') as file:
        json.dump(text, file)

    answer = input('\nРаспечатать количество полученных вакансий? (press Enter to deny): ')
    if answer:
        with open(json_file, 'r') as file:
            print(len(json.load(file)))


if __name__ == '__main__':
    main(searching_for)
