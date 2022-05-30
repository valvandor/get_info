import json
import os

from HH_search import const
from HH_search.hh_search import make_fully_hh_search



def main():
    searching_text = input('What?\n')

    if not os.path.exists(f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}'):
        os.mkdir(f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}')

    text = searching_text.strip()
    searched = text.replace(' ', '_')

    json_file = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{searched}{const.FILE_EXTENSION}'
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(
            make_fully_hh_search(text), file)

    searched_text_file = f'{const.ROOT_DIRECTORY}{const.DATA_DIRECTORY}{const.FILE_LAST_SEARCHED_TEXT}'
    with open(searched_text_file, 'w', encoding='utf-8') as file:
        json.dump({const.SEARCHED_TEXT: text}, file)

    answer = input('\nРаспечатать количество полученных вакансий? (press Enter to deny): ')
    if answer:
        with open(json_file, 'r') as file:
            print(len(json.load(file)))


if __name__ == '__main__':
    main()
