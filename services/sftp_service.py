import logging
import time

import paramiko

from config import config


class SFTPService:
    def __init__(self):
        self.transport = paramiko.Transport((config.sftp_host, config.sftp_port))
        self.transport.connect(username=config.sftp_username, password=config.sftp_password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def watch_log_file(self, logs_path, handler):
        try:
            with self.sftp.file(logs_path, 'r') as logfile:
                logfile.seek(0, 2)
                while True:
                    line = logfile.readline()
                    if not line:
                        time.sleep(1)
                        continue
                    message = handler.handle(line)
                    if message:
                        yield message

        except Exception as e:
            logging.error(f"Error watching log file: {e}")

        finally:
            self.sftp.close()
            self.transport.close()
