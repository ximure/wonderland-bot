import os
import time

import paramiko
from dotenv import load_dotenv

import line_handler
import telegram_handler

load_dotenv()

username = os.getenv('SFTP_USERNAME')
password = os.getenv('SFTP_PASSWORD')
host = os.getenv('SFTP_HOST')
port = int(os.getenv('SFTP_PORT'))
logs_path = '/logs/latest.log'

transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

try:
    with sftp.file(logs_path, 'r') as logfile:
        logfile.seek(0, 2)

        while True:
            line = logfile.readline()
            if not line:
                time.sleep(1)
                continue
            message = line_handler.handle(line)
            telegram_handler.send_message(message)

finally:
    sftp.close()
    transport.close()
