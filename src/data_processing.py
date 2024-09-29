def find_significant_drops(ticker_data, thresholds):
    """
    Найти монеты с падением на заданные пороги.

    :param ticker_data: Данные тикера Poloniex
    :param thresholds: Список порогов (например, [10, 30, 50])
    :return: Словарь с порогами и соответствующими монетами
    """
    significant_drops = {threshold: [] for threshold in thresholds}
    for coin, data in ticker_data.items():
        try:
            percent_change = float(data.get("percentChange", "0"))
            if percent_change <= -thresholds[0]:
                for threshold in thresholds:
                    if percent_change <= -threshold:
                        significant_drops[threshold].append({
                            "name": coin,
                            "volume": data.get("baseVolume", "0")
                        })
            elif percent_change >= thresholds[0]:
                # Можно добавить логику для восстановления цены, если необходимо
                pass
        except ValueError:
            continue
    return significant_drops
