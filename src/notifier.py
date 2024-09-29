from src.poloniex_api import get_ticker_data
from src.database import get_all_users
from src.data_processing import find_significant_drops
from src.telegram_bot import updater
from src.handlers import send_telegram_message

def job():
    ticker_data = get_ticker_data()
    users = get_all_users()
    for user in users:
        thresholds = user['thresholds']
        drops = find_significant_drops(ticker_data, thresholds)
        message = format_message(drops)
        if message:
            send_telegram_message(updater, user['chat_id'], message)

def format_message(drops):
    message = "📉 Найдены монеты с резким падением и восстановлением:\n"
    for threshold, coins in drops.items():
        if coins:
            message += f"\n🔹 Изменение более чем на {threshold}%:\n"
            for coin in coins:
                message += f"• {coin['name']} - Объем торгов: {coin['volume']}\n"
    return message if message != "📉 Найдены монеты с резким падением и восстановлением:\n" else ""
