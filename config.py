import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.sftp_username = os.getenv('SFTP_USERNAME')
        self.sftp_password = os.getenv('SFTP_PASSWORD')
        self.sftp_host = os.getenv('SFTP_HOST')
        self.sftp_port = int(os.getenv('SFTP_PORT'))
        self.environment = os.getenv('ENVIRONMENT', 'DEV')

        if self.environment == 'DEV':
            self.telegram_token = os.getenv('TELEGRAM_DEV_TOKEN')
            self.telegram_chat_id = os.getenv('TELEGRAM_DEV_CHAT_ID')
        else:
            self.telegram_token = os.getenv('TELEGRAM_PROD_TOKEN')
            self.telegram_chat_id = os.getenv('TELEGRAM_PROD_CHAT_ID')

        self.rcon_host = os.getenv('RCON_HOST')
        self.rcon_port = int(os.getenv('RCON_PORT'))
        self.rcon_password = os.getenv('RCON_PASSWORD')


config = Config()
