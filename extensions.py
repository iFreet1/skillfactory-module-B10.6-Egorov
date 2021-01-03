import requests
import json
from config import currency_keys


class ConvertException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise ConvertException('Параметры конвертируемых валют не могут быть равны')

        try:
            base_ticker = currency_keys[base]
        except Exception as e:
            raise ConvertException('Невозможно обработать валюту, цену которой надо узнать')

        try:
            quote_ticker = currency_keys[quote]
        except Exception as e:
            raise ConvertException('Невозможно обработать валюту, в которой надо узнать цену')

        try:
            amount = float(amount)
        except Exception as e:
            raise ConvertException('Невозможно обработать количество конвертируемой валюты')

        result = requests.get(f'https://api.exchangeratesapi.io/latest?'
                              f'base={currency_keys[quote]}&symbols={currency_keys[base]}')
        convert_value = json.loads(result.content)['rates'][currency_keys[base]] * amount
        convert_value = round(convert_value, 2)

        return convert_value
