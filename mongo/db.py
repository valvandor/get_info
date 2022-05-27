from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

vacancies_connector = client.vacancies
