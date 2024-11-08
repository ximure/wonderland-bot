import logging
import threading

from bots.telegram_listener import run_listener
from handlers.line_handler import LineHandler
from handlers.telegram_handler import TelegramHandler
from services.sftp_service import SFTPService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def start_sftp_watcher():
    try:
        sftp_service = SFTPService()
        line_handler = LineHandler()
        telegram_handler = TelegramHandler()
        sftp_service.watch_log_file('/logs/latest.log', line_handler, telegram_handler)
    except Exception as ex:
        logging.error(f"Error in SFTP watcher: {ex}")


if __name__ == '__main__':
    try:
        sftp_thread = threading.Thread(target=start_sftp_watcher)
        sftp_thread.start()
        run_listener()
    except Exception as e:
        logging.error(f"Error in main: {e}")
