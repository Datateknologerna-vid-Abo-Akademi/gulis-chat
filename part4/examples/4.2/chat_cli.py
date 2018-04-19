import time
import urllib2
import json
import threading

server_url = "http://37.59.100.46:10080"
last_message_id = 0


def print_messages(json_string):
    global last_message_id

    try:
        parsed = json.loads(json_string)
    except ValueError:
        return

    if isinstance(parsed, list):
        for message in parsed:
            print("{}: {}".format(message['sender'], message['content']))
            if int(message['id']) > last_message_id:
                last_message_id = int(message['id'])
    elif isinstance(parsed, dict):
        if "error" not in parsed:
            print("{}: {}".format(parsed['sender'], parsed['content']))
            if int(parsed['id']) > last_message_id:
                last_message_id = int(parsed['id'])
        else:
            print("An error has occurred: {}".format(parsed['error']))


def get_past(server, channel, count=50):
    try:
        response = urllib2.urlopen(
            "{}/past?channel={}&count={}".format(server, channel, count))
        return response.read()
    except urllib2.HTTPError, error:
        return error.read()


def get_new(server, channel, last):
    try:
        response = urllib2.urlopen(
            "{}/get?channel={}&last={}".format(server, channel, last))
        return response.read()
    except urllib2.HTTPError, error:
        return error.read()


def update(server, channel, interval, thread_lock):
    global last_message_id
    while True:
        with thread_lock:
            new = get_new(server, channel, last_message_id)
            print_messages(new)
        time.sleep(interval)


chat_channel = str(raw_input("Enter channel: ")).strip()
if len(chat_channel) == 0:
    print("You must enter a channel!")
    exit(1)

chat_name = str(raw_input("Enter your name: ")).strip()
if len(chat_name) == 0:
    print("You must enter a name!")
    exit(1)

print("Hello {}, connecting to channel '{}'...".format(chat_name, chat_channel))

data = get_past(server_url, chat_channel)

print_messages(data)

lock = threading.Lock()

updateThread = threading.Thread(target=update, args=(server_url, chat_channel, 2, lock))

updateThread.daemon = True

updateThread.start()

while True:
    raw_input()
    with lock:
        inp = raw_input("Write message: ")
        print(inp)
