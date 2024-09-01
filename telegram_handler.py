import os

import requests
from dotenv import load_dotenv

token = ''
chat_id = ''
load_dotenv()

if os.getenv('ENVIRONMENT') == 'DEV':
    token = os.getenv('TELEGRAM_DEV_TOKEN')
    chat_id = os.getenv('TELEGRAM_DEV_CHAT_ID')
elif os.getenv('ENVIRONMENT') == 'PROD':
    token = os.getenv('TELEGRAM_PROD_TOKEN')
    chat_id = os.getenv('TELEGRAM_PROD_CHAT_ID')

send_message_url = 'https://api.telegram.org/bot' + token + '/sendMessage'

def send_message(message):
    requests.post(
        url=send_message_url,
        data=
        {
            'chat_id': chat_id,
            'text': message
        }
    ).json()
