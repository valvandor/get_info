import json

from hh_search import make_fully_hh_search_by_word

search_word = 'python'

file_path = f'{search_word}_vacancies.json'

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(
        make_fully_hh_search_by_word(search_word), file)

answer = input('\nРаспечатать количество полученных вакансий? (press Enter to deny): ')
if answer:
    with open(file_path, 'r') as file:
        print(len(json.load(file)))
