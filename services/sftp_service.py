import logging
import time
from threading import Timer

import paramiko

from config import config


class SFTPService:
    def __init__(self):
        self.sftp = None
        self.transport = None
        self.cache = []
        self.cache_interval = 3
        self.timer = None
        self.connect()

    def connect(self):
        try:
            self.transport = paramiko.Transport((config.sftp_host, config.sftp_port))
            self.transport.connect(username=config.sftp_username, password=config.sftp_password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            logging.info("Successfully connected to SFTP server.")
        except Exception as e:
            logging.error(f"Error connecting to SFTP server: {e}")
            self.sftp = None
            self.transport = None

    def start_cache_timer(self, telegram_handler):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.cache_interval, self.flush_cache, [telegram_handler])
        self.timer.start()

    def flush_cache(self, telegram_handler):
        if self.cache:
            message_block = "".join(self.cache)
            telegram_handler.send_message(message_block)
            self.cache.clear()

    def watch_log_file(self, logs_path, handler, telegram_handler):
        while True:
            logs_file = self.sftp.file(logs_path, 'r')
            initial_files_count = len(self.sftp.listdir("./logs"))
            logs_file.seek(0, 2)
            self.start_cache_timer(telegram_handler)

            while True:
                line = logs_file.readline()
                current_files_count = len(self.sftp.listdir("./logs"))

                if initial_files_count != current_files_count:
                    logging.info(f"Current files count changes from {initial_files_count} to {current_files_count}. Reopening logs file")
                    break
                
                if not line:
                    time.sleep(1)
                    continue

                message = handler.handle(line)

                if message:
                    self.cache.append(message)

                if self.cache:
                    self.start_cache_timer(telegram_handler)
