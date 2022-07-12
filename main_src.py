import re
import numpy as np
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import flask
from flask import Flask, request
from flask_sslify import SSLify

url = 'https://VVVRSN.pythonanywhere.com/'
bot = telebot
bot.remove_webhook()
bot.set_webhook(url=url)

app = Flask(name)
ssl = SSLify(app)


@app.route('/' + secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


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
        
        #getting price as numbers 
        price = float(re.search(r'\d+.\d+', price_line).group(0))
        sl = float(re.search(r'\d+.\d+', sl_line).group(0))
    except:
        return 'Wrong input'

    
    #calculating tp1, tp2, tp3
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

    return('\n'.join(converted_message_lines))


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


_token = '1185538777:AAELBkaBLISFXiq2RPoXeWg7hv0CxCZ_p6A'

updater = Updater(token=_token, use_context=True)
dispatcher = updater.dispatcher


SIGNAL_RECIEVED, CANCEL = 1, 0

def signal_command_recieved(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Now, send me a signal')
    return SIGNAL_RECIEVED


def signal_received(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=convert_message(update.message.text))
    return CANCEL


def tp1_received(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=hit_tp1(update.message.text))
    return CANCEL


def tp2_received(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=hit_tp2(update.message.text))
    return CANCEL


def tp3_received(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=hit_tp3(update.message.text))
    return CANCEL


def add_keyboard(update, context):
    custom_keyboard = [['/signal'], 
                    ['/tp1', '/tp2', '/tp3'],
                    ['/kdel']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text="Keyborad added", reply_markup=reply_markup)


def del_keyboard(update, context):
    reply_markup = telegram.ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.message.chat_id, text="Keyboard removed", reply_markup=reply_markup)

    
def cancel_conversation():
    return ConversationHandler.END


add_keyboard_handler = CommandHandler('kadd', add_keyboard)

del_keyboard_handler = CommandHandler('kdel', del_keyboard)

cancel_handler = CommandHandler('cancel', cancel_conversation)

signal_handler = ConversationHandler(
    entry_points=[CommandHandler('signal', signal_command_recieved)],
    states={
        SIGNAL_RECIEVED: [MessageHandler(Filters.text, signal_received)],
        CANCEL: [cancel_handler]
        },
    fallbacks = [cancel_handler],
    allow_reentry=True
    )

tp1_handler = ConversationHandler(
    entry_points=[CommandHandler('tp1', signal_command_recieved)],
    states={
        SIGNAL_RECIEVED: [MessageHandler(Filters.text, tp1_received)],
        CANCEL: [cancel_handler]
        },
    fallbacks = [cancel_handler],
    allow_reentry=True
    )

tp2_handler = ConversationHandler(
    entry_points=[CommandHandler('tp2', signal_command_recieved)],
    states={
        SIGNAL_RECIEVED: [MessageHandler(Filters.text, tp2_received)],
        CANCEL: [cancel_handler]
        },
    fallbacks = [cancel_handler],
    allow_reentry=True
    )

tp3_handler = ConversationHandler(
    entry_points=[CommandHandler('tp3', signal_command_recieved)],
    states={
        SIGNAL_RECIEVED: [MessageHandler(Filters.text, tp3_received)],
        CANCEL: [cancel_handler]
        },
    fallbacks = [cancel_handler],
    allow_reentry=True
    )

dispatcher.add_handler(add_keyboard_handler)
dispatcher.add_handler(del_keyboard_handler)
dispatcher.add_handler(signal_handler)
dispatcher.add_handler(tp1_handler)
dispatcher.add_handler(tp2_handler)
dispatcher.add_handler(tp3_handler)


if __name__ == '__main__':
    app.run()
# updater.start_polling()
updater.idle()
    