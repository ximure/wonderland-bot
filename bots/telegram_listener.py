import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils.formatting import Text

from config import config
from handlers.telegram_handler import TelegramHandler
from message_type import MessageType
from services.rcon_service import RCONService

bot = Bot(token=config.telegram_token)
dp = Dispatcher()
rcon_service = RCONService()
telegram_handler = TelegramHandler()


async def handle_message(message: Message):
    try:
        if str(message.chat.id) == config.telegram_chat_id:
            message_type = telegram_handler.detect_message_type(message)
            message_sender_username = message.from_user.username if message.from_user else "Unknown"
            message_formatter = "§o"

            if message_type == MessageType.TEXT:
                telegram_message = message.text
            elif message_type == MessageType.STICKER:
                telegram_message = f"{message_formatter}отправил стикер (эмодзи): {message.sticker.emoji}"
            elif message_type == MessageType.VOICE:
                telegram_message = f"{message_formatter}отправил голосовое сообщение"
            elif message_type == MessageType.VIDEO_NOTE:
                telegram_message = f"{message_formatter}отправил видеосообщение"
            elif message_type == MessageType.PHOTO:
                telegram_message = f"{message_formatter}отправил фото"
            elif message_type == MessageType.AUDIO:
                telegram_message = f"{message_formatter}отправил аудио"
            elif message_type == MessageType.DOCUMENT:
                telegram_message = f"{message_formatter}отправил документ"
            elif message_type == MessageType.REPLY:
                reply_message = message.reply_to_message.text
                sent_message = message.text

                if reply_message is not None:
                    telegram_message = f"{message_formatter}'{reply_message}' -> '{sent_message}'"
                else:
                    telegram_message = f"{message_formatter}ответил на стикер или что-то другое, не текстовое"
            elif message_type == MessageType.FORWARD:
                telegram_message = f"{message_formatter}переслал сообщение"
            else:
                telegram_message = f"{message_formatter}отправил сообщение неизвестного типа"

            rcon_service.send_command(telegram_message, message_sender_username)
    except Exception as e:
        logging.error(f"Error handling message: {message} - {e}")


@dp.message(Text)
async def handle_telegram_message(message: Message):
    await handle_message(message)


async def start_telegram_listener():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error starting Telegram listener: {e}")


def run_listener():
    asyncio.run(start_telegram_listener())
