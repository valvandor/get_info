import json
import requests
from pprint import pprint
from config import settings

# There's The Open Movie Database
URL = 'http://www.omdbapi.com/'

# Find all movies with words in the title
includes_in_title = 'valve'
# Get credential info (that's should be your own key)
app_key = settings.get('APP_KEY_FOR_OMDBAPI')

params = {'apikey': app_key,
          's': includes_in_title,
          }

response = requests.get(URL, params=params)
json_data = response.json()

if json_data['Response']:
    searched_movie = json_data['Search']
    file_name = f'results_for"{includes_in_title}"'
    with open(f'{file_name}.json', 'w') as file:
        json.dump(searched_movie, file)
else:
    print('Nothing found')
