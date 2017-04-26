
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

    # return the response to Facebook.
    return response()

def type_handler(messenger_parser, user):
    # Send coordinates message to receive the user's current location
    send_categories_message(user.messenger_id, 'Please choose from the following categories of news: International, Sports, Tech & Science, Entertainment, Business, Daily')
     
    # Change the user state to ask_source so the next time the user sends a message, it asks for what source of news they want
    user.state = 'ask_source'
    user.save()

def source_handler(user)

    # Send message asking where the user wants to go
    send_source_message(user.messenger_id, 'Which of the following sources do you want to read:')

    if messenger_parser.text == 'International': 
       send_message(user.messenger_id, '') #put sources in
    elif messenger_parser.text == 'Sports': 
       send_message(user.messenger_id, '') #put sources in
    elif messenger_parser.text == 'Tech' or 'Science' or 'Tech & Science': 
       send_message(user.messenger_id, '') #put sources in    
    elif messenger_parser.text == 'Entertainment': 
       send_message(user.messenger_id, '') #put sources in
    elif messenger_parser.text == 'Business': 
       send_message(user.messenger_id, '') #put sources in
    elif messenger_parser.text == 'Daily': 
       send_message(user.messenger_id, '') #put sources in
    else: 
       send_message(user.messenger_id, 'Please choose from the following categories of news: International, Sports, Tech & Science, Entertainment, Business, Daily')

    # Change the user state to give_result so the next time the user sends a message, it gives what rideshare is cheaper.
    user.state = 'ask_order'
    user.save()

def order_handler(messenger_parser, user):
    send_order_message(user.messenger_id, 'Do you want to read the top news, the latest news, or the most popular news?')
    

def results_handler(messenger_parser, user):
     
