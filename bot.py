
# Script that houses main logic of bot
from messenger_parser import MessengerParser
from news_api_requests import suggested_articles
from messenger_api_requests import send_message
from helpers import response
from db import User


def response_handler(request):
     # Parse request and get the data we want out of it like messenger_id, text, and coordinates.
    messenger_parser = MessengerParser(request)

    # Get user object from database so we can see the state of our user.
    try:
        user = User.select().where(User.messenger_id == messenger_parser.messenger_id).get()
    except:
        # If user doesn't exist, we create them. This would be a first time user.
        user = User.create(messenger_id=messenger_parser.messenger_id, state='ask_type')
        
    # Here we need to decide what we need to do next for our user
    if user.state == 'ask_type':
        # ask user what type of news (tech, sports, etc)
        type_handler(messenger_parser, user)
    elif user.state == 'ask_source':
        # ask user what source
        source_handler(messenger_parser, user)
    elif user.state == 'ask_order':
        # ask order (top, popular, latest)
        order_handler(messenger_parser, user)
    else:
        #get results
        results_handler(user)

    # We are all done so just return the typical response to Facebook.
    return response()

