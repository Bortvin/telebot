import telebot
from telebot import types
import configure

bot = telebot.TeleBot(configure.config['token'])

settings = {
    "keywords": {
        "yes": [],
        "no": [],
    },
    "users": {
        "yes": [],
        "no": [],
    },
    "commands": {
        "keys": {
            "desc": "* Ключевые слова *\n", # описание
            "key_add": "/key_add <первое слово> <второе слово> ...\n",
            "key_see": "/key_see посмотреть все ключевые слова\n",
            "key_rm": "/key_rm <первое слово> <второе слово> ...\n",
            "key_rm_all": "/key_rm очистить весь список слов\n",
        },
        "users": {
            "desc": "* Пользовательские команды *\n", # описание
            "users_add": "/users_add <первый id> <второй id>\n",
            "users_see": "/users_see посмотреть всех пользователей\n",
            "users_rm": "/users_rm <первый id> <второй id>\n",
            "users_rm_all": "/users_rm_all очистить весь список пользователей\n",
        },
    }
}

'''
    settings
        ключевые слова
            добавить
            удалить
            показать все ключевые слова
            назад
        пользователи
            назад
        доп. ностройки
            назад
'''
'''
@bot.message_handler(commands=['settings'])
def get_user_info(msg):
    keyBoard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btn_keyWords = types.KeyboardButton("Ключевые слова")
    btn_users = types.KeyboardButton("Пользователи")
    btn_extraSet = types.KeyboardButton("Доп. настройки")
    keyBoard.add(btn_keyWords)
    keyBoard.row(btn_users)
    keyBoard.row(btn_extraSet)
    bot.reply_to(msg, "Настройки:", reply_markup=keyBoard)

@bot.message_handler(commands=['help'])
def send_help(msg):
    pass

@bot.message_handler(content_types=["text"])
def bot_message(msg):
    if msg.text == 'Ключевые слова':
        keyBoard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        btn_add = types.KeyboardButton("Добавить ключевые слова")
        btn_remove = types.KeyboardButton("Удалить ключевые слова")
        btn_show = types.KeyboardButton("Показать ключевые слова")
        btn_back = types.KeyboardButton("Назад в меню")
        keyBoard.add(btn_add)
        keyBoard.row(btn_remove)
        keyBoard.row(btn_show)
        keyBoard.row(btn_back)
        bot.reply_to(msg, 'Ключевые слова', reply_markup=keyBoard)
    elif msg.text == 'Пользователи':
        keyBoard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        btn_add = types.KeyboardButton("Добавить в списки пользователей")
        btn_remove = types.KeyboardButton("Удалить пользователей")
        btn_show = types.KeyboardButton("Показать список пользователей")
        btn_back = types.KeyboardButton("Назад в меню")
        keyBoard.row(btn_add)
        keyBoard.row(btn_remove)
        keyBoard.row(btn_show)
        keyBoard.row(btn_back)
        bot.reply_to(msg, 'Пользователи', reply_markup=keyBoard)
    elif msg.text == 'Доп. настройки':
        keyBoard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        btn_back = types.KeyboardButton("Назад в меню")
        keyBoard.row(btn_back)
        bot.reply_to(msg, 'Доп. настройки', reply_markup=keyBoard)
    elif msg.text == 'Назад в меню':
        keyBoard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        btn_keyWords = types.KeyboardButton("Ключевые слова")
        btn_users = types.KeyboardButton("Пользователи")
        btn_extraSet = types.KeyboardButton("Доп. настройки")
        keyBoard.add(btn_keyWords)
        keyBoard.row(btn_users)
        keyBoard.row(btn_extraSet)
        bot.reply_to(msg, "Настройки:", reply_markup=keyBoard)
    elif msg.text == "Добавить ключевые слова":
        pass
    else:
        pass
         # checking sentence

'''


# general
@bot.message_handler(commands="help")
def help(msg):
    str = []
    for key1, val1 in settings['commands'].items():
        for key2, val2 in settings["commands"][key1].items():
            str += [val2]

    bot.send_message(msg.chat.id, ''.join(str))

# ========================

# key_words
@bot.message_handler(commands="key_add")
def key_add(msg):
    words = msg.text.split(' ')
    words.pop(0)
    settings["keywords"]["yes"] += words
    bot.send_message(msg.chat.id, 'Слова успешно добавлены')

@bot.message_handler(commands="key_see")
def key_see(msg):
    keys = ', '.join(settings['keywords']['yes'])
    bot.send_message(msg.chat.id, f"Ваш список ключевых слов:\n{keys}")

@bot.message_handler(commands="key_rm")
def key_rm(msg):
    words = msg.text.split(' ')
    words.pop(0)
    keys = settings['keywords']['yes']
    for key in keys:
        if key in words:
            keys.remove(key)
    bot.send_message(msg.chat.id, 'Слова успешно удалены')

@bot.message_handler(commands="key_rm_all")
def key_rm_all(msg):
    settings['keywords']['yes'].clear()
    bot.send_message(msg.chat.id, 'Список очищен')

# ========================

# ================ users ===================

@bot.message_handler(commands="users_add")
def users_add(msg):
    words = msg.text.split(' ')
    words.pop(0)
    settings["users"]["yes"] += words
    bot.send_message(msg.chat.id, 'ID успешно добавлены')


@bot.message_handler(commands="users_see")
def users_see(msg):
    users = ', '.join(settings['users']['yes'])
    bot.send_message(msg.chat.id, f"Ваш список пользователей:\n{users}")

@bot.message_handler(commands="users_rm")
def users_rm(msg):
    words = msg.text.split(' ')
    words.pop(0)
    users = settings['users']['yes']
    for key in users:
        if key in words:
            users.remove(key)
    bot.send_message(msg.chat.id, 'ID успешно удалены')

@bot.message_handler(commands="users_rm_all")
def users_rm_all(msg):
    settings['users']['yes'].clear()
    bot.send_message(msg.chat.id, 'список ID очищен')

# =======================

@bot.message_handler(content_types=['text'])
def parse_text(msg):
    # msg.from_user.id => id пользователя
    # msg.from_user.username => username пользователя

    # bot.send_message(msg.chat.id, msg.chat.get_member(1866869901))
    pass


@bot.message_handler(commands=["key_add", "key_rm", "key_see", "key_rm_all"])
def check(msg):
    if "key_add" in msg.text:
         words = msg.text.split(' ')
         words.pop(0)
         settings["keywords"]["yes"] += words
         bot.send_message(msg.chat.id, 'Слова успешно добавлены')
    elif msg.text == "/key_rm":
        words = msg.text.split(' ')
        words.pop(0)
        keys = settings['keywords']['yes']

        for key in keys:
            if key in words:
                keys.remove(key)

        bot.send_message(msg.chat.id, 'Слова успешно удалены')
    elif msg.text == "/key_see":
        keys = ', '.join(settings['keywords']['yes'])
        bot.send_message(msg.chat.id, f"Ваш список ключевых слов:\n{keys}")
    elif msg.text == "/key_rm_all":
        settings['keywords']['yes'].clear()
        bot.send_message(msg.chat.id, 'Список очищен')
'''
'''

def check(msg, keywords, request):
    for i in range(len(keywords)):
        if keywords[i] in request:
            return True
    return False

@bot.message_handler(content_types = ['text'])
def parse_it(msg):
    request = msg.text.lower()
    #bot.send_message(msg.chat.id, "hi")
    res = check(msg, settings["keywords"], request)
    if res == True:
        bot.send_message(msg.chat.id, "здесь есть что-то важное!")
    else:
        bot.send_message(msg.chat.id, "не вижу ничего интересного")



bot.polling(none_stop = True, interval=0)