import json


def load_from_file(path):
    with open(path, 'r') as file:
        return json.load(file)
