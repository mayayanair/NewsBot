# Script to send API requests to News API
import requests

# Constants
NEWS_API_KEY = '1c9c265acc9a44fd8e597a83b238896a'
NEWS_URL = 'https://newsapi.org/v1/articles'

def articles(source):
    # Package params into dictionary for GET request.
    params = {
        'apiKey':NEWS_API_KEY,
        'source': source
    }

    # Send POST request to News API
    r = requests.get(NEWS_URL, params=params)

    # Check if success, if success, return translated text. If not, return error message.
    if r.status_code != 200:
        return 'Something wrong happened, try again later!'

    text = r.json()['articles']
    return text
