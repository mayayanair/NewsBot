
# Script that houses main logic of bot
from messenger_parser import MessengerParser
from news_api_requests import suggested_articles
from messenger_api_requests import send_message
from helpers import response


def response_handler(request):
    # Grabs JSON request and makes it MessengerParser object for easy use
    received_message = MessengerParser(request)

    # Uses suggested_articles function in news_api_requests.py to get the articles
    translation = translate_message(received_message.text, TARGET_LANGUAGE)

    # Uses send_message function in messenger_parser.py to send translated message back to user
    send_message(received_message.messenger_id, translation)

    # Ends FB's webhook request with a response with a 200 success code
    return response()
