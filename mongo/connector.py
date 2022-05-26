from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db_connector = client.db_info
