
# Script to send messages to FB Messenger via FB Messenger Send API
import requests

# Constants
FB_ACCESS_TOKEN = 'EAADtxV351YoBABxqxXzpehpJ8FKXPS5w8XQ5KD4EaNNREQqmjeUyunpAVd7dJhqAZCMCQ3svIdS0ZAY3W7kYaUtiJjzPmMf8XqYEHrsxCnQhHjHIYqmNyvkD40qAKKpD4BfqTwl9Ctoe4UrIO3WFvx2ZB9YQ9L0GDuy9XkAZAgZDZD'
SEND_API_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + 'EAADtxV351YoBABxqxXzpehpJ8FKXPS5w8XQ5KD4EaNNREQqmjeUyunpAVd7dJhqAZCMCQ3svIdS0ZAY3W7kYaUtiJjzPmMf8XqYEHrsxCnQhHjHIYqmNyvkD40qAKKpD4BfqTwl9Ctoe4UrIO3WFvx2ZB9YQ9L0GDuy9XkAZAgZDZD'

def send_message(messenger_id, text):
    # Package params into dictionaries for POST request
    recipient = {'id':messenger_id}
    message = {'text':text}
    params = {
        'recipient':recipient,
        'message':message
    }

    # Send POST request to Facebook Messenger Send API to send text message
    r = requests.post(SEND_API_URL, json=params)
    
def send_categories_message(messenger_id, text, categories):
    # Package params into dictionaries for POST request
    quick_replies = [] # append to
    for c in categories:
        # https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies
        '''
        {
            "content_type":"text",
            "title":"CATEGORY NAME",
            "payload":"CATEGORY NAME"
        }
        '''
        quick_replies.append({"content_type":"text", "title":c,"payload":c})

    recipient = {'id':messenger_id}
    message = {
        'text':text,
        'quick_replies':quick_replies
    }
    params = {
        'recipient':recipient,
        'message':message
    }

    # Send POST request to Facebook Messenger Send API to send coordinates message
    r = requests.post(SEND_API_URL, json=params)
