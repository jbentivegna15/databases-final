import requests
import json

def get_horoscope(sign):
    """
    This function calls a public horoscope API to get a daily horoscope
    """

    api_url_base = 'http://horoscope-api.herokuapp.com'

    headers = {
        'Content-Type': 'application/json'
    }

    api_url = api_url_base + '/horoscope/today/' + sign

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None