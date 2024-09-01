import logging

from mcrcon import MCRcon

from config import config


class RCONService:
    def __init__(self):
        self.rcon_host = config.rcon_host
        self.rcon_port = config.rcon_port
        self.rcon_password = config.rcon_password

    def send_command(self, command):
        print(f'пока не работает. Команда: {command}')
        # try:
        #     with MCRcon(self.rcon_host, self.rcon_password, port=self.rcon_port) as mcr:
        #         response = mcr.command(command)
        #         logging.info(f"RCON Response: {response}")
        #         return response
        # except Exception as e:
        #     logging.error(f"Error sending RCON command: {command} - {e}")
        #     return None
