chat_channel = str(raw_input("Enter channel: ")).strip()
if len(chat_channel) == 0:
    print("You must enter a channel!")
    exit(1)

chat_name = str(raw_input("Enter your name: ")).strip()
if len(chat_name) == 0:
    print("You must enter a name!")
    exit(1)

print("Hello {}, connecting to channel '{}'...".format(chat_name, chat_channel))


