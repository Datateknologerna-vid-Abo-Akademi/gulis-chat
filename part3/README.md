# Part 3

Finally, the time has come, to start coding!

In this part, the objective is to start writing a simple program with a command line interface (CLI) for communicating with the server.

**Note**: We will be writing this in Python 2.7, but if you want to use a newer version, remember, Google is your friend!

## 3.1 The plan

The plan is to create a program, which eventually, on start asks for the channel to connect to and then your name.

After that the program gets the past 50 messages and after that with 2 second intervals gets new messages.

If you write something, the program listens and eventually send your message when return is pressed.

## 3.2 The base

Okay, let's start by creating a program that you can enter the channel and your name in to.

```python
chat_channel = str(raw_input("Enter channel: ")).strip()
if len(chat_channel) == 0:
    print("You must enter a channel!")
    exit(1)

chat_name = str(raw_input("Enter your name: ")).strip()
if len(chat_name) == 0:
    print("You must enter a name!")
    exit(1)

print("Hello {}, connecting to channel '{}'...".format(chat_name, chat_channel))
```

## 3.3 GETing messages

Now that we have our channel and name saved, let's get the 50 last messages.
We do this using `urllib2`, it should come installed with Python.

```python
import urllib2
response = urllib2.urlopen(url)
data = response.read()
```

To perform a `GET` request, we only pass the URL to the `urlopen()` function.
To understand what the URL should look like, we can use Insomnia.

Open the `past` request in Insomnia, that we created in [Part 1](../part1/README.md).

In the Query tab, enter a channel of your choice and set the value for `count` to 50. Now you can test the query by clicking Send in the upper bar.

Just above the parameters in the Query tab, we have a box called `URL PREVIEW` where we see what the final `GET` query URL looks like. This is what we want to send with `urllib2`.

Of course you need to change the channel to whatever the user enters and the count could also be a variable instead of a static number.

If you print out the returned data, the output should look something like this:

```text
Enter channel: test
Enter your name: otto
Hello otto, connecting to channel 'test'...
[{"id":1,"channel":"test","sender":"Otto","content":"Hello World 2","time":"2018-04-16T07:54:09Z"},{"id":2,"channel":"test","sender":"Otto","content":"Hello Universe","time":"2018-04-16T07:54:52Z"}]
```

[Example code](examples/3.3/chat_cli.py)

## 3.4 Parsing JSON

As we know, the server responds with JSON formatted data. It is not very user friendly to display raw JSON data, so we must do something to make it look better.

To work with JSON in Python, we need to import `json`. To read a JSON object or array to Python understandable format, we use `json.loads()` and `json.dumps()`.

Reading a JSON string would be done like this:

```python
import json
pythonUnderstandableJSON = json.loads('{"key": "value"}')
value = pythonUnderstandableJSON['key']
```

Easy enough! Let's add this functionality to our program. I made a function for printing the messages which also handles possible errors:

```python
def print_messages(json_string):
    try:
        parsed = json.loads(json_string)
    except ValueError:
        return

    if isinstance(parsed, list):
        for message in parsed:
            print("{}: {}".format(message['sender'], message['content']))
    elif isinstance(parsed, dict):
        if "error" not in parsed:
            print("{}: {}".format(parsed['sender'], parsed['content']))
        else:
            print("An error has occurred: {}".format(parsed['error']))
```

**Pro tip!** Play around with the Insomnia REST client and see what response bodies and codes the server returns.

Next we will add getting new messages. If you are stuck, take a look at the [example code](examples/3.4/chat_cli.py).

## 3.5 Fetching new messages

As we know, the `/get` endpoint on the server needs the `channel` parameter and optionally a parameter `last`. The parameter `last` is the message ID that you last received, meaning the server returns only messages that have been sent after that.

We obviously don't want all messages every time, so we will save the last message ID locally and send it to the server when getting new messages.

I added simple checkups in my `print_messages` function that compare the messages ID with the saved one. If the message has a higher ID than what we have saved, overwrite the saved ID.

```python
last_message_id = 0

def print_messages(json_string):
    global last_message_id  # Access the variable stored outside the function

    try:
        parsed = json.loads(json_string)
    except ValueError:
        return

    if isinstance(parsed, list):
        for message in parsed:
            print("{}: {}".format(message['sender'], message['content']))
            # Check if bigger ID than stored
            if int(message['id']) > last_message_id:
                last_message_id = int(message['id'])
    elif isinstance(parsed, dict):
        if "error" not in parsed:
            print("{}: {}".format(parsed['sender'], parsed['content']))
            # Check if bigger ID than stored here too
            if int(parsed['id']) > last_message_id:
                last_message_id = int(parsed['id'])
        else:
            print("An error has occurred: {}".format(parsed['error']))
```

To access variables from outside a function, use `global variable_name` inside the function.

If you didn't frite a function for getting past messages, it is recommended to do that, at least for getting **new** messages.

Here is what my function for getting new messages looks like:

```python
def get_new(server, channel, last):
    try:
        response = urllib2.urlopen(
            "{}/get?channel={}&last={}".format(server, channel, last))
        return response.read()
    except urllib2.HTTPError, error:
        return error.read()
```

It is usually smart to split the program into functions and classes, as this makes the software more modular and therefore easier to maintain.

That said, now it is easy to create a function for continuously get new messages.

My `get_new` function took an argument `last`. Therefore my updating function looks like this:

```python
def update(server, channel, interval):
    global last_message_id
    while True:
        new = get_new(server, channel, last_message_id)
        print_messages(new)
        time.sleep(interval)    # seconds
```

Note again the `global` variable. This ensures we don't get too much unnecessary data.

The `update` function will run indefinitely, so we call it at the end of our program, at least for now.

```python
update(server_url, chat_channel, 2)
```

Now it will get new messages every 2 seconds. You can test this by sending a message with Insomnia.

So far my program looks like [this](examples/3.5/chat_cli.py).

## 3.6 Conclusion

We will continue creating our CLI chat client in the next part. There we will learn about threads and try to clean our client to make it more modular.

Check the [examples directory](examples/) if you get stuck with something, but as always, try to do it yourself first.

Think about what impact the update interval has on the user and the server.
What if there are a hundred, a thousand or a million clients?
Would you be okay with only receiving new messages once a minute?