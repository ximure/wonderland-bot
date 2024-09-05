import logging
import re


class LineHandler:
    player_message_regex = '^\[\d{2}:\d{2}:\d{2}] \[Server thread\/INFO]: (?!\[Not Secure\])(ximure (joined the game|left the game)|<ximure> .+)'

    @staticmethod
    def handle(line):
        try:
            if not re.search(LineHandler.player_message_regex, line):
                return None

            return line[33:]

        except Exception as e:
            logging.error(f"Error handling line: {line} - {e}")
            return None
