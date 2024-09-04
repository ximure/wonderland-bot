import logging

import requests

from config import config
from message_type import MessageType


class TelegramHandler:
    def __init__(self):
        self.token = config.telegram_token
        self.chat_id = config.telegram_chat_id
        self.send_message_url = f'https://api.telegram.org/bot{self.token}/sendMessage'

    def send_message(self, message):
        try:
            response = requests.post(
                url=self.send_message_url,
                data={'chat_id': self.chat_id, 'text': message}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error sending message to Telegram: {e}")
            return None

    def detect_message_type(self, message):
        if message.sticker:
            return MessageType.STICKER
        elif message.voice:
            return MessageType.VOICE
        elif message.video_note:
            return MessageType.VIDEO_NOTE
        elif message.photo:
            return MessageType.PHOTO
        elif message.audio:
            return MessageType.AUDIO
        elif message.document:
            return MessageType.DOCUMENT
        elif message.reply_to_message:
            return MessageType.REPLY
        elif message.forward_from:
            return MessageType.FORWARD
        elif message.text:
            return MessageType.TEXT
        else:
            return MessageType.OTHER
