import logging
import re


class LineHandler:
    player_message_regex = '\[.+] \[Server thread\/INFO]: (<.+> .+|.+ joined the game|.+ left the game|.+ has made the advancement \[.+])'

    @staticmethod
    def handle(line):
        try:
            if not re.search(LineHandler.player_message_regex, line):
                return None

            return line[33:]

        except Exception as e:
            logging.error(f"Error handling line: {line} - {e}")
            return None
