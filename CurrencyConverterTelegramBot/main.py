import telebot.types
from settings import TOKEN, keys
from extensions import APIException, CheckInput, Parser

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):

    text = 'Бот для конвертации валют.\n\n \
Для начала работы введите сообщение в следующем формате:\n \
<имя валюты, которую хотите перевести>\n \
<имя валюты, в которую хотите перевести>\n \
<количество переводимой валюты>\n  \
Пример: рубль доллар 1\n\n Если желаете посмотреть доступные валюты, введите: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):

    text = 'Доступные валюты:'
    for k in keys.keys():
        text = '\n'.join((text, k))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    try:
        quote, base, amount = CheckInput.check_input(message.text)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')

    else:
        result = Parser.get_price(quote, base, amount)
        quote, base, amount = message.text.lower().split()
        text = f'Цена {amount} {quote} в {base} = {result}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
