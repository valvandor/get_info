from connector import vacancies_connector
from dao_vacancy import DAOVacancy
from helpers import load_from_file

vacancies = vacancies_connector.vacancies
vacancies_service = DAOVacancy(vacancies)

vacancies_data = load_from_file('../HH_search/python_vacancies.json')

vacancies_service.insert(vacancies_data)
