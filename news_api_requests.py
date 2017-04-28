# Script to send API requests to Google API's
import requests

# Constants
NEWS_API_KEY = '1c9c265acc9a44fd8e597a83b238896a'
NEWS_URL = 'https://newsapi.org/v1/articles'

def suggested_articles(source,apiKey):
    # Package params into dictionary for GET request.
    params = {
        'key':NEWS_API_KEY, #ASK ROBERT if we need to restate api key here if its already defined above!!!!!!!
        's': source
    }

    # Send POST request to Google.
    r = requests.get(NEWS_URL, params=params)

    # Check if success, if success, return translated text. If not, return error message.
    if r.status_code != 200:
        return 'Something wrong happened, try again later!'

    text = r.json()['data']['translations'][0]['translatedText'] # ASK ROBERT what this will return !!!!!!!!!!!
    return text
