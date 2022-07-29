import telebot
from config import keys, TOKEN
from extensions import APIExcepton, CriptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def echo_test(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следущем формате:\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIExcepton("Слишком много параметров.")

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except APIExcepton as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}.")
    else:
        new_price = round((float(amount) * float(total_base)),4)
        text = f"Цена {amount} {quote} в {base} - {new_price}"
        bot.send_message(message.chat.id, text)


bot.polling()