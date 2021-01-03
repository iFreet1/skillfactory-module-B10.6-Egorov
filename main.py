import telebot
from config import TOKEN, currency_keys
from extensions import Converter, ConvertException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    help_data = 'Для работы с ботом введите данные валют в следующем формате:\n' \
                '<имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты> ' \
                '<количество первой валюты>\n' \
                'Чтобы показать список валют доступных для конвертации, введите /values'
    bot.send_message(message.chat.id, help_data)


@bot.message_handler(commands=['values'])
def currency(message: telebot.types.Message):
    currency_data = 'Доступные для конвертации валюты:\n'

    for value in currency_keys:
        currency_data += f'{value}\n'

    bot.reply_to(message, currency_data)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        input_data = str.lower(message.text).split()

        if len(input_data) > 3:
            raise ConvertException('Слишком много параметров')
        elif len(input_data) < 3:
            raise ConvertException('Слишком мало параметров')

        base, quote, amount = input_data

        convert_value = Converter.get_price(base, quote, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка ввода - {e}')
    except Exception as e:
        bot.reply_to(message, f'Необрабатываемая команда - {e}')
    else:
        bot.send_message(message.chat.id, f'Цена "{quote}" в "{base}" - {convert_value}')


bot.polling()
