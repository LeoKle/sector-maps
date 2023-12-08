import requests

from data.settings import load_url


def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_data():
    url = load_url()
    return fetch_json(url)
