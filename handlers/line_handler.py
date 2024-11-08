import logging
import re


class LineHandler:
    player_message_regex = '^\[\d{2}:\d{2}:\d{2}] \[Server thread\/INFO]: (?!\[Not Secure\])(ximure (joined the game|left the game)|<ximure> .+)'

    @staticmethod
    def handle(line):
        try:
            message_string = line[33:]
            if not re.search(LineHandler.player_message_regex, line):
                return None
            if message_string.startswith("@"):
                LineHandler.handle_command(message_string)
            else:
                return message_string
        except Exception as e:
            logging.error(f"Error handling line: {line} - {e}")
            return None


    def handle_command(line):
        logging.debug(f"handle_command(): processing {line} command")
