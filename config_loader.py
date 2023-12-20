import json


def load_config(path):
    with open(path, 'r') as file:
        return json.load(file)
