import datetime
import os
import requests
import json


# API_URL = os.environ['CONVERTER_API']

class CoinbaseHandler:
    # TODO добавить абстрактный класс
    def __init__(self, cache_handler):
        self.__cache_handler = cache_handler

    @staticmethod
    def form_response(status, message):
        return {"status": status, "message": message}

    def get_rate(self, from_currency="BTC", to_currency="UAH"):
        try:
            current_rate = json.loads(self.__cache_handler.get_cache("current_rate"))
        except TypeError:
            current_rate = None
        if current_rate:
            time_between_insertion = datetime.datetime.now() - datetime.datetime.fromisoformat(current_rate['time'])
            if time_between_insertion.seconds < 30:
                return CoinbaseHandler.form_response(200, current_rate)

        r = requests.get(f'https://api.coinbase.com/v2/prices/{from_currency}-{to_currency}/buy')
        rate = r.json()['data']
        rate['time'] = datetime.datetime.now()
        self.__cache_handler.set_cache("current_rate", json.dumps(rate, default=str))
        print(rate)
        return CoinbaseHandler.form_response(200, rate)
