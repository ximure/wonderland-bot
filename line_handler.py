import re

player_message_regex = '\[.+] \[Server thread\/INFO]: (<.+> .+|.+ joined the game|.+ left the game|.+ has made the advancement \[.+])'

def handle(line):
    if not re.search(player_message_regex, line):
        return

    return line[33:]
