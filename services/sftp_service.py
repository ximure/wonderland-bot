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

    def reconnect(self):
        self.close()
        self.connect()

    def close(self):
        if self.sftp:
            self.sftp.close()

        if self.transport:
            self.transport.close()

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
            try:
                if self.sftp is None:
                    logging.warning("SFTP connection lost. Reconnecting...")
                    self.reconnect()

                with self.sftp.file(logs_path, 'r') as logfile:
                    logfile.seek(0, 2)
                    self.start_cache_timer(telegram_handler)

                    while True:
                        line = logfile.readline()
                        if not line:
                            time.sleep(1)
                            continue

                        message = handler.handle(line)

                        if message:
                            self.cache.append(message)

                        if self.cache:
                            self.start_cache_timer(telegram_handler)

            except Exception as e:
                logging.error(f"Error watching log file: {e}. Reconnecting...")
                self.reconnect()
                time.sleep(5)

            finally:
                self.flush_cache(telegram_handler)
                self.close()
