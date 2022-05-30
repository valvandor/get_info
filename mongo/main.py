import json

from mongo.const import DIR_DATA
from mongo.db import client, use_collection
from mongo.dao_vacancy import DAOVacancy
from mongo.helpers import load_from_file
import const


# if __name__ == '__main__':
#     main()
#

def get_searched_word():
    with open(f'{DIR_DATA}{const.FILE_LAST_SEARCHED_TEXT}', 'r') as file:
        data = (json.load(file))
        search_text = data[const.SEARCHED_TEXT]
    return search_text


search_text = get_searched_word()

vacancies_db = client.vacancies
python_vacancies_collection = use_collection(f'{search_text}_vacancies', vacancies_db)
python_vacancies_service = DAOVacancy(python_vacancies_collection)

file_path = f'{DIR_DATA}{search_text}_vacancies.json'
python_vacancies_data = load_from_file(file_path)
python_vacancies_service.insert(python_vacancies_data)
