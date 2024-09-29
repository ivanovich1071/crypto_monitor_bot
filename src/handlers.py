from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from src.database import add_user, update_user_thresholds, get_user_thresholds
from src.notifier import format_message
import logging

logger = logging.getLogger(__name__)

def setup_handlers(updater):
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("report", report))

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    add_user(chat_id)
    keyboard = [
        [InlineKeyboardButton(">50%", callback_data='50')],
        [InlineKeyboardButton(">30%", callback_data='30')],
        [InlineKeyboardButton(">10%", callback_data='10')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Добро пожаловать! Выберите диапазоны колебаний котировок, по которым вы хотите получать отчёты:",
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    threshold = int(query.data)
    update_user_thresholds(chat_id, threshold)
    query.edit_message_text(text=f"Вы выбрали диапазон изменения более чем на {threshold}%.")

def report(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    thresholds = get_user_thresholds(chat_id)
    if not thresholds:
        update.message.reply_text("Вы не выбрали ни один диапазон. Пожалуйста, используйте /start для выбора.")
        return
    from src.poloniex_api import get_ticker_data
    from src.data_processing import find_significant_drops
    ticker_data = get_ticker_data()
    drops = find_significant_drops(ticker_data, thresholds)
    message = format_message(drops)
    if message:
        update.message.reply_text(message)
    else:
        update.message.reply_text("Нет монет, соответствующих выбранным диапазонам.")

def send_telegram_message(updater, chat_id, message):
    updater.bot.send_message(chat_id=chat_id, text=message)
