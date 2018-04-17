import urllib2
import json

server_url = "http://37.59.100.46:10080"


def print_messages(json_string):
    try:
        parsed = json.loads(json_string)
    except ValueError:
        return

    if isinstance(parsed, list):
        for message in parsed:
            print("{}: {}".format(message['sender'], message['content']))
    else:
        if "error" not in parsed:
            print("{}: {}".format(parsed['sender'], parsed['content']))
        else:
            print("An error has occurred: {}".format(parsed['error']))


def get_past(channel, count=50):
    global server_url
    try:
        response = urllib2.urlopen(
            "{}/past?channel={}&count={}".format(server_url, channel, count))
        return response.read()
    except urllib2.HTTPError, error:
        return error.read()


chat_channel = str(raw_input("Enter channel: ")).strip()
if len(chat_channel) == 0:
    print("You must enter a channel!")
    exit(1)

chat_name = str(raw_input("Enter your name: ")).strip()
if len(chat_name) == 0:
    print("You must enter a name!")
    exit(1)

print("Hello {}, connecting to channel '{}'...".format(chat_name, chat_channel))

data = get_past(chat_channel)

print_messages(data)


