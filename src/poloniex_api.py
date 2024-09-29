import requests
import logging
from src.config import POLONIEX_API_URL
from requests.exceptions import RequestException

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)


def get_ticker_data():
    """
    Получает данные о тикерах с Poloniex API.

    :return: Словарь с данными тикеров или пустой словарь при ошибке.
    """
    url = f"{POLONIEX_API_URL}?command=returnTicker"
    try:
        response = requests.get(url, timeout=10)  # Устанавливаем таймаут 10 секунд
        response.raise_for_status()  # Вызывает HTTPError для плохих ответов (4xx или 5xx)
        data = response.json()
        logger.info("Успешно получены данные тикеров с Poloniex.")
        return data
    except RequestException as e:
        # Обработка всех исключений, связанных с запросом
        logger.error(f"Ошибка при запросе к Poloniex API: {e}")
    except ValueError as e:
        # Обработка ошибок декодирования JSON
        logger.error(f"Ошибка декодирования JSON от Poloniex API: {e}")
    except Exception as e:
        # Обработка всех остальных исключений
        logger.error(f"Неизвестная ошибка: {e}")

    # Возврат пустого словаря в случае ошибки
    return {}
