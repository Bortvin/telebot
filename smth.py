import os

def code_os():
    if not os.path.exists("folder"):
        os.mkdir("folder")
    else:
        print("exists")

def search(text, pattern):
    arr = text.split(' ')
    if pattern in arr:
        print(1)
    else:
        print(0)

def key_add(message):
    words = message.split(' ')
    words = ' '.join(words[1:])
    words = words.split(';')
    for i in range(len(words)):
        words[i] = words[i].strip()
    return words

print(key_add("/key_add красный крест; что-то; затем это"))



#return 0