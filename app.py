import telebot
from config import money, TOKEN
from extensions import ConvertException, MoneyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helps(message: telebot.types.Message):
    text = 'Чтобы начать работу введите в именительном падеже:' \
           '\n - Имя валюты из которой нужно перевести' \
           '\n - Имя валюты в которую нужно перевести' \
           '\n - Количество переводимой валюты' \
           '\n Список всех доступных валют:/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in money.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertException('Параметров больше трёх')

        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        total_base = float(total_base) * float(amount)
        text = f'Цена {amount} {quote} в {base} = {"%.2f" % total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()

