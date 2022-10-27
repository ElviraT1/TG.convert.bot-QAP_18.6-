import telebot
from сonfig import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! Я Forex-bot. Вот, что я умею: \n\n1) Конвертировать валюту с помощью команды:' \
           '\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>. ' \
           '\n Вводите значения строчными буквами через пробел. Например: "рубль доллар 1000".' \
           '\n2) Показывать список всех доступных валют с помощью команды /values.' \
           '\n3) Напомнить, что я умею с помощью команды /help\n\nНачнем? Введите команду:'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionException('Введите команду или 3 параметра')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except CryptoConverter as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Перевожу {quote} в {base}.\n{amount} {quote} = {total_base} {base}.' \
               f'\n\nЧтобы конвертировать новую валюту введите команду: <имя валюты>' \
               f' <в какую валюту перевести> <количество переводимой валюты>.'
        bot.send_message(message.chat.id, text)


bot.polling()
