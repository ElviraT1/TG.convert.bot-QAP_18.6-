import requests
import json
from сonfig import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
         if quote == base:
            raise ConvertionException(f'Не могу перевести одинаковые валюты {base}.')

         try:
            quote_ticker = keys[quote]
         except KeyError:
            raise ConvertionException(f'Не знаю такую валюту - {quote}. Попробуйте ввести другую.')

         try:
            base_ticker = keys[base]
         except KeyError:
            raise ConvertionException(f'Не знаю такую валюту - {base}. Попробуйте ввести другую.')

         try:
            amount = float(amount)
         except ValueError:
             raise ConvertionException(f'Ой, что-то не так с количеством {amount}. Попробуйте еще раз.')

         r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
         total_base = float(json.loads(r.content)[keys[base]]) * amount

         return total_base
