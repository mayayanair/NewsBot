
# Script to send messages to FB Messenger via FB Messenger Send API
import requests

# Constants
FB_ACCESS_TOKEN = 'EAADtxV351YoBAP5Ue6AU9KgkMdKjF4n9FQ6RSMWWGIS2pZAqagRIpSwQLL8De3QYIXWHpPoNEKBOl0m6YkeJaHdohBWhw96e5vY7azuXZBtDhfZBe5mcgVNDM2CphZA0r5ZBdfxAw9CiPNif9a9lvLbhWb2PsDflSKMVhYzcwGwZDZD'
SEND_API_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAADtxV351YoBAP5Ue6AU9KgkMdKjF4n9FQ6RSMWWGIS2pZAqagRIpSwQLL8De3QYIXWHpPoNEKBOl0m6YkeJaHdohBWhw96e5vY7azuXZBtDhfZBe5mcgVNDM2CphZA0r5ZBdfxAw9CiPNif9a9lvLbhWb2PsDflSKMVhYzcwGwZDZD'

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
