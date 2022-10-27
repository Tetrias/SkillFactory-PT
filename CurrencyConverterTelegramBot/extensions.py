import json
import requests
from settings import keys


# Собственное исключение для проверки ввода пользователя.
class APIException(Exception):
    pass


# Класс проверки и вывода соответствующего исключения.
class CheckInput:

    @staticmethod
    def check_input(message):

        message = message.lower().split()

        if len(message) != 3:
            raise APIException('Несоответствие количества значений с ожидаем.')
        if message[0] == message[1]:
            raise APIException(f'Невозможно перевести одинаковые валюты.')

        try:
            checked_quote = keys[message[0]]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {message[0]}.')

        try:
            checked_base = keys[message[1]]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {message[1]}.')

        try:
            checked_num = float(message[2])
        except ValueError:
            raise APIException(f'Не удалось обработать число: {message[2]}')
        return checked_quote, checked_base, checked_num


# Получение результата из API.
class Parser:

    @staticmethod
    def get_price(quote, base, amount):

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base}&from={quote}&amount={amount}"
        payload = {}
        headers = {"apikey": ""}
        response = requests.request("GET", url, headers=headers, data=payload)
        result = json.loads(response.content)

        return result['result']
