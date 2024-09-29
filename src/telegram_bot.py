from telegram.ext import Updater

from src.config import TELEGRAM_BOT_TOKEN

# Инициализация Updater
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
