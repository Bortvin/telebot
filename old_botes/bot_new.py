import telebot
from telebot import types
import configure

bot = telebot.TeleBot(configure.config['token'])

@bot.message_handler(commands=['greet', 'hello'])  # получает список компанды
def get_user_info(msg):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text = 'да', callback_data='yes')
    item_no = types.InlineKeyboardButton(text = 'нет', callback_data='no')

    markup_inline.add(item_yes, item_no)
    bot.send_message(msg.chat.id, 'да или нет?',
        reply_markup = markup_inline
    )

bot.callback_query_handler(func = lambda call: True)
#bot.answer_callback_query()
def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_id = types.KeyboardButton('мой id')
        item_username = types.KeyboardButton('мой ник')

        markup_reply.add(item_id, item_username)
        bot.send_message(call.msg.chat.id, 'Нажмите на одну из кнопок',
            reply_markup = markup_reply
        )
    elif call.data == 'no':
        pass

def check(msg, keywords, request):
    for i in range(len(keywords)):
        if keywords[i] in request:
            return True
    return False

@bot.message_handler(content_types = ['text'])
def parse_it(msg):
    request = msg.text.lower().split()
    keywords = ["важное", "д/з"]
    # bot.send_message(msg.chat.id, ' '.join(request))
    res = check(msg, keywords, request)
    if res == True:
        bot.send_message(msg.chat.id, "здесь есть что-то важное!")
    else:
        bot.send_message(msg.chat.id, "не вижу ничего интересного")

'''
     if msg.text == 'мой id':
bot.send_message(msg.chat.id, f'Your ID: {msg.from_user.id}')
    elif msg.text == 'мой ник':
bot.send_message(msg.chat.id, f'Your ID: {msg.from_user.first_name} {msg.from_user.last_name}')
'''

bot.polling(none_stop = True, interval=0)

'''
    закреплял
'''