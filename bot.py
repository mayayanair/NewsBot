
# Script that houses main logic of bot
from messenger_parser import MessengerParser
from news_api_requests import articles
from messenger_api_requests import send_message, send_categories_message
from helpers import response
from db import User
from send import GenericTemplateMessage, GenericTemplateElement, URLButton 

POLITICS = ['Breitbart News']
SPORTS = ['BBC Sport','ESPN','ESPN Cric Info','Football Italia','FourFourTwo','Fox Sports','NFL News','TalkSport','The Sport Bible']
TECHNOLOGY = ['Ars Technica','Hacker News','Recode','T3n','TechCrunch','TechRadar','The Next Web','The Verge','Wired.de']
ENTERTAINMENT = ['Buzzfeed','Daily Mail','Entertainment Weekly','Mashable','The Lad Bible']
SCIENCE_AND_NATURE = ['National Geographic','New Scientist']
MUSIC = ['MTV News','MTV News UK']
GAMING = ['IGN','Polygon']
BUSINESS = ['Bloomberg','Business Insider','CNBC', 'Financial Times','Fortune','The Economist','The Wall Street Journal']
GENERAL = ['Al Jazeera','Associated Press','BBC News','CNN','New York Magazine','The Guardian','The Huffington Post','The New York Times','The Telegraph','The Times of India','The Washington Post']


SOURCE_TEXT_TO_API_FRIENDLY_SOURCE_NAME = {
    'ABC News':'abc-news-au','Al Jazeera':'al-jazeera-english','Ars Technica':'ars-technica','Associated Press':'associated-press','BBC News':'bbc-news','BBC Sport':'bbc-sport','Bild':'bild','Bloomberg':'bloomberg','Breitbart News':'breitbart-news','Business Insider':'business-insider','Business Insider UK':'business-insider-uk','Buzzfeed':'buzzfeed','CNBC':'cnbc','CNN':'cnn','Daily Mail':'daily-mail','Der Tagesspiegel':'der-tagesspiegel','Die Zeit':'die-zeit','Engadget':'endadget','Entertainment Weekly':'entertainment-weekly','ESPN':'espn','ESPN Cric Info':'espn-cric-info','Financial Times':'financial-times','Focus':'focus','Football Italia':'football-italia','Fortune':'fortune','FourFourTwo':'four-four-two','Fox Sports':'fox-sports','Google News':'google-news','Gruenderszene':'gruenderszene','Hacker News':'hacker-news','Handelsblatt':'handelsblatt','IGN':'ign','Independent':'independent','Mashable':'mashable','Metro':'metro','Mirror':'mirror','MTV News':'mtv-news','MTV News UK':'mtv-news-uk','National Geographic':'national-geographic','New Scientist':'new-scientist','Newsweek':'newsweek','New York Magazine':'new-york-magazine','NFL News':'nfl-news','Polygon':'polygon','Recode':'recode','Reddit':'reddit-r-all','Reuters':'reuters','Spiegel Online':'spiegel-online','T3n':'t3n','TalkSport':'talksport','TechCrunch':'techcrunch','TechRadar':'techradar','The Economist':'the-economist','The Guardian':'the-guardian-au','The Guardian UK':'the-guardian-uk','The Hindu':'the-hindu','The Huffington Post':'the-huffington-post','The Lad Bible':'the-lad-bible','The New York Times':'the-new-york-times','The Next Web':'the-next-web','The Sport Bible':'the-sport-bible','The Telegraph':'the-telegraph','The Times of India':'the-times-of-india','The Verge':'the-verge','The Wall Street Journal':'the-wall-street-journal','The Washington Post':'the-washington-post','Time':'time','USA Today':'usa-today','Wired.de':'wired-de','Wirtschafts Woche':'wirtschafts-woche'
}

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
    else:
        # call api and get results
        results_handler(messenger_parser,user)

    # return the response to Facebook.
    return response()

def type_handler(messenger_parser, user):
    # Send coordinates message to receive the user's current location
    send_message(user.messenger_id, 'Please choose from the following categories of news: Politics, Sports, Technology, Entertainment, Science and Nature, Music, Gaming, Business, General')
     
    # Change the user state to ask_source so the next time the user sends a message, it asks for what source of news they want
    user.state = 'ask_source'
    user.save()

def source_handler(messenger_parser, user):

    # Send message asking where the user wants to go
    #send_source_message(user.messenger_id, 'Which of the following sources do you want to read:')
    sources_text = 'Which of the following sources do you want to read: '

    if messenger_parser.text.lower() == 'politics': 
        send_categories_message(user.messenger_id, sources_text, POLITICS) # repeat this for everything
    elif messenger_parser.text.lower() == 'sports': 
        send_categories_message(user.messenger_id, sources_text, SPORTS)
    elif messenger_parser.text.lower() == 'technology': 
        send_categories_message(user.messenger_id, sources_text, TECHNOLOGY)   
    elif messenger_parser.text.lower() == 'entertainment': 
        send_categories_message(user.messenger_id, sources_text, ENTERTAINMENT)
    elif messenger_parser.text.lower() == 'science and nature': 
        send_categories_message(user.messenger_id, sources_text, SCIENCE_AND_NATURE)
    elif messenger_parser.text.lower() == 'music': 
        send_categories_message(user.messenger_id, sources_text, MUSIC)
    elif messenger_parser.text.lower() == 'gaming': 
        send_categories_message(user.messenger_id, sources_text, GAMING)
    elif messenger_parser.text.lower() == 'business': 
        send_categories_message(user.messenger_id, sources_text, BUSINESS)
    elif messenger_parser.text.lower() == 'general': 
        send_categories_message(user.messenger_id, sources_text, GENERAL)
    else:
        type_handler(messenger_parser, user)
        return
    # Change the user state to give_result so the next time the user sends a message, it gives what rideshare is cheaper.
    user.state = 'results_handler'
    user.save()

def results_handler(messenger_parser, user):
    text = messenger_parser.text
    if SOURCE_TEXT_TO_API_FRIENDLY_SOURCE_NAME.get(text):
        # grab that value from dictionary and then do news api 
        result = articles(SOURCE_TEXT_TO_API_FRIENDLY_SOURCE_NAME[text])
        elements = []
        count = 0 
        for a in result:
            if count > 10:
                break
            title = a['title']
            item_url = a['url']
            image_url = a['urlToImage']

            b = URLButton('Read Article', item_url)
            elements.append(GenericTemplateElement(title, item_url, image_url, '', [b])) 
            count += 1

        mess = GenericTemplateMessage(elements, user.messenger_id)
        mess.send()
        user.state = 'ask_type'
        user.save()
    else:
        source_handler(messenger_parser, user)
     
