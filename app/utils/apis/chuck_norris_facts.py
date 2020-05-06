import requests
import json
from flask import current_app

def get_chuck_norris_facts():
    url = 'https://api.chucknorris.io/jokes/random'
    r = requests.get(url)
    return json.loads(r.text)