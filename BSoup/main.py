import json
from pprint import pprint

from hh_search import make_fully_hh_search_by_word

search_word = 'python'

with open(f'{search_word}_vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(
        make_fully_hh_search_by_word(search_word), file)

answer = input('Распечатать? (press Enter to deny)\n')
if answer:
    with open('vacancies.json', 'r') as file:
        pprint(json.load(file))
