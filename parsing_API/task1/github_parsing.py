import requests
import json

user_login = 'valvandor'
URL = f'https://api.github.com/users/{user_login}/repos'

response = requests.get(URL)
json_data = response.json()

repository_names = [repo['name'] for repo in json_data]

file_name = 'repo-names'
with open(f'{file_name}.json', 'w') as file:
    json.dump(repository_names, file)

