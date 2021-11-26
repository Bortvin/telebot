import logging
import configure
import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = configure.config["token"]
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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
            "key_add": "/key_add <первое слово>; <второе слово>; ...\n",
            "key_see": "/key_see посмотреть все ключевые слова\n",
            "key_rm": "/key_rm <первое слово>; <второе слово>; ...\n",
            "key_rm_all": "/key_rm_all очистить весь список слов\n",
        },
        "users": {
            "desc": "* Пользовательские команды *\n", # описание
            "users_add": "/users_add <первый id>; <второй id>;\n",
            "users_see": "/users_see посмотреть всех пользователей\n",
            "users_rm": "/users_rm <первый id>; <второй id>;\n",
            "users_rm_all": "/users_rm_all очистить весь список пользователей\n",
        },
    }
}

# Functions
def divideByWords(msg): # get a string
    words = msg.split(' ')
    words = ' '.join(words[1:])
    words = words.split(';')
    for i in range(len(words)):
        words[i] = words[i].strip()
    return words[:len(words)-1]

def search(text, pattern):
    text = text.split()
    if pattern in text:
        return 1
    else:
        return 0
#

# General comands
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    str = []
    for key1, val1 in settings['commands'].items():
        for key2, val2 in settings["commands"][key1].items():
            str += [val2]
    await message.answer(''.join(str))

# key commands
@dp.message_handler(commands=['key_add'])
async def key_add(message: types.Message):
    words = divideByWords(message.text)
    if len(words) <= 0:
        await message.answer('Нечего добавить в список')
    else:
        settings["keywords"]["yes"] += words
        settings["keywords"]["yes"] = list(set(settings["keywords"]["yes"])) # убираем повторы
        await message.answer(f'Слова успешно добавлены')


@dp.message_handler(commands="key_see")
async def key_see(message: types.Message):
    keys = ', '.join(settings['keywords']['yes'])
    if len(keys) == 0:
        keys = '(пусто)'
    await message.answer(f"Ваш список ключевых слов:\n{keys}")


@dp.message_handler(commands="key_rm")
async def key_rm(message: types.Message):
    words = divideByWords(message.text)
    if (len(' '.join(words)) > 1):
        keys = settings['keywords']['yes']
        for key in keys:
            if key in words:
                keys.remove(key)
        await message.answer('Слова успешно удалены')
    else:
        await message.answer('Нечего удалить')

@dp.message_handler(commands="key_rm_all")
async def key_rm_all(message: types.Message):
    settings['keywords']['yes'].clear()
    await message.answer('Список очищен')

# users_commands

@dp.message_handler(commands='users_add')
async def users_add(message: types.Message):
    words = divideByWords(message.text)
    if len(words) <= 0:
        await message.answer('Нечего добавить в список')
    else:
        settings["users"]["yes"] += words
        settings["users"]["yes"] = list(set(settings["users"]["yes"]))  # убираем повторы
        await message.answer(f'usernames успешно добавлены')

@dp.message_handler(commands='users_see')
async def users_see(message: types.Message):
    users = ', '.join(settings['users']['yes'])
    if len(users) == 0:
        users = '(пусто)'
    await message.answer(f"username пользователей:\n{users}")

@dp.message_handler(commands='users_rm')
async def users_rm(message: types.Message):
    words = message.text.strip().replace(";", "").split(' ')
    words = words[1:]
    # await message.answer(f'{words} {len(words)}')
    if (len(' '.join(words)) > 0):
        users = settings['users']['yes']
        for user in users:
            if user in users:
                users.remove(user)
        await message.answer('usernames успешно удалены')
    else:
        await message.answer('Нечего удалить')

@dp.message_handler(commands='users_rm_all')
async def users_rm_all(message: types.Message):
    settings['users']['yes'].clear()
    await message.answer('Список очищен')

# getting message

@dp.message_handler()
async def echo(message: types.Message):
   # await message.answer(message.from_user.username)
    username = '@' + message.from_user.username
    important_username = False
    important_msg = False

    if username in settings["users"]["yes"]:
        important_username = True

    keys = settings["keywords"]["yes"]
    for key in keys:
        if search(message.text, key):
            important_msg = True
            break

    if important_username or important_msg:
        await message.pin(disable_notification=False)
        await message.reply('Важное сообщение:', disable_notification=False)
        #await message.answer(f'{username} writes: "{message.text}"', disable_notification=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)