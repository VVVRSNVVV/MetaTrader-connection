import re
import numpy as np
import telebot
from telebot import types
from flask import Flask, request
from flask_sslify import SSLify


def convert_message(message):
    # decoration
    buy_sticker = '📈'
    sell_sticker = '📉'
    fire_sticker = '💥'
    hashtags = '#forextracker #signal'
    dot = '•'

    # tp1, tp2, tp3 template
    tps_buy = np.array([0.0020, 0.0050, 0.0100])
    tps_sell = np.array([-0.0020, -0.0050, -0.0100])

    message = message.replace('VVVRSN', 'snoopDoggyDog')

    # search for needed values
    to_buy = 'buy' in message.lower()
    try:
        price_line = re.search(r'price.+\d+\.\d+', message.lower()).group(0)
        sl_line = re.search(r'sl.+\d+\.\d+', message.lower()).group(0)
        pair = re.search(r'[# ][A-Z]{6} ', message).group(0)
        pair = re.search(r'[A-Z]{6}', pair).group(0)

        # getting price as numbers
        price = float(re.search(r'\d+.\d+', price_line).group(0))
        sl = float(re.search(r'\d+.\d+', sl_line).group(0))
    except:
        return 'Wrong input'

    # calculating tp1, tp2, tp3
    tps = tps_buy + price if to_buy else tps_sell + price

    sticker = buy_sticker if to_buy else sell_sticker
    action = 'BUY' if to_buy else 'SELL'

    converted_message_lines = [
        f'{sticker} {action} #{pair} {fire_sticker}',
        hashtags,
        '',
        f'Price: {price:.4f}',
        '',
        f'TP1 {dot} {tps[0]:.4f}',
        f'TP2 {dot} {tps[1]:.4f}',
        f'TP3 {dot} {tps[2]:.4f}',
        '',
        f'SL {dot} {sl:.4f}'
    ]

    return ('\n'.join(converted_message_lines))


def hit_tp1(message):
    hit_text = f'HIT TP1 2️⃣0️⃣ pips+ 🔥 🤑'

    try:
        pair = re.search(r'[# ][A-Z]{6} ', message).group(0)
        pair = re.search(r'[A-Z]{6}', pair).group(0)
    except:
        return 'Wrong input'

    return f'#{pair} {hit_text}'


def hit_tp2(message):
    hit_text = f'HIT TP2 5️⃣0️⃣ pips+ 🔥 🤑'

    try:
        pair = re.search(r'[# ][A-Z]{6} ', message).group(0)
        pair = re.search(r'[A-Z]{6}', pair).group(0)
    except:
        return 'Wrong input'

    return f'#{pair} {hit_text}'


def hit_tp3(message):
    hit_text = f'HIT TP3 1️⃣0️⃣0️⃣ pips+ 🔥 🤑'

    try:
        pair = re.search(r'[# ][A-Z]{6} ', message).group(0)
        pair = re.search(r'[A-Z]{6}', pair).group(0)
    except:
        return 'Wrong input'

    return f'#{pair} {hit_text}'

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_signal = types.KeyboardButton('signal')
btn_tp1 = types.KeyboardButton('tp1')
btn_tp2 = types.KeyboardButton('tp2')
btn_tp3 = types.KeyboardButton('tp3')
keyboard.add(btn_signal, btn_tp1,btn_tp2, btn_tp3)

secret = 'hellobitch'
token = '1185538777:AAELBkaBLISFXiq2RPoXeWg7hv0CxCZ_p6A'
url = 'https://VVVRSN.pythonanywhere.com/'
bot = telebot.TeleBot(token, threaded=False)
# bot.remove_webhook()
# bot.set_webhook(url=url)

app = Flask(__name__)
ssl = SSLify(app)


@app.route('/' + secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@app.route('/' + secret, methods=['GET'])
def index():
    return '<h1>Bot</h1>'


@bot.message_handler(commands=['start'])
def start_func(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,'Choose button..', reply_markup=keyboard)


@bot.message_handler()
def button_click(message):
    if message.text == 'signal':
        bot.send_message(message.chat.id, 'send me a message')
        @bot.message_handler()
        def signal_b(message):
            bot.send_message(message.chat.id, convert_message(message.text))
    elif message.text == 'tp1':
        bot.send_message(message.chat.id, 'send me a message')
        @bot.message_handler()
        def signal_b(message):
            bot.send_message(message.chat.id, hit_tp1(message.text))
    elif message.text == 'tp2':
        bot.send_message(message.chat.id, 'send me a message')
        @bot.message_handler()
        def signal_b(message):
            bot.send_message(message.chat.id, hit_tp2(message.text))
    elif message.text == 'tp3':
        bot.send_message(message.chat.id, 'send me a message')
        @bot.message_handler()
        def signal_b(message):
            bot.send_message(message.chat.id, hit_tp3(message.text))


bot.polling()

if __name__ == '__main__':
    app.run()
