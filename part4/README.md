# Part 4

In this part we continue creating our CLI chat client by adding message sending.

To be able to do multiple things at the same time, such as writing a message and getting new ones, we need threads, so that's what we'll look at next.

## 4.1 Threads

Last time, we created a function `update`, that with 2 second intervals looked for new messages.

Now, we want to create a thread for this function, so it runs in the background and lets us move on in our main program.

In Python, threads are created by the `threading` package, so let's import it:

```python
import threading
```

To create a thread, we do:

```python
my_thread = threading.Thread(target=function_name, args=(arg1, arg2))
```

Next, we need to start our thread. If we do it now, the thread will run in the background even if our main program exits.
In this application we do not want this, therefore we add the following:

```python
my_thread.daemon = True
```

Now, we can start our thread:

```python
my_thread.start()
```

Try doing this with our `update` function.

At this point, our program will terminate after it has started the thread. This is because there is nothing more tu run on the main thread, therefore it exits.

We can fix this by adding an infinite loop at the end:

```python
my_thread.start()

while True:
    pass
```

With our loop in place, the program should continuously fetch new messages.

## 4.2 Thread locks

Add the following to the end of our program, after where we start our thread:

```python
while True:
    inp = raw_input("Write message: ")
    print(inp)
```

If you now run the program, we should get `Write message:` and if we write something, it should print to the terminal and ask you to write another message.

What happens if you from Insomnia send a message to the server while inputting in your program?

The problem we have now, is we need a way to pause getting and printing new messages while we write our message. This can easily be achieved with a `lock`.

To create a lock, simply do the following:

```python
my_lock = threading.Lock()
```

The lock basically acts as a pause mechanism. Only one thing at the time can run inside the lock. In Python we can do stuff inside a locked state, by running what we need inside a `with` statement.

If we were to add a lock to our message writing activity, it would look something like this:

```python
while True:
    with my_lock:
        inp = raw_input("Write message: ")
        print(inp)
```

and the `update` would look like this (we must have a lock there too, only then we can have only one of them running at once):

```python
def update(server, channel, interval, thread_lock):
    global last_message_id
    while True:
        with thread_lock:
            new = get_new(server, channel, last_message_id)
            print_messages(new)
        time.sleep(interval)    # Not inside lock
```

**Note** that the `time.sleep(interval)` is not inside the lock, otherwise we have to wait the interval before the lock is released. You can try this.

However, this will always lock the state for writing a message, and we still want to get updates when not writing.

Luckily, the `raw_input` method waits until something is entered, meaning we can put it before our lock:

```python
while True:
    raw_input() # Wait for Enter to be pressed before locking
    with my_lock:
        inp = raw_input("Write message: ")
        print(inp)
```

Now, when pressing Enter on our keyboard while listening for new messages, we enter the "write message"-mode. After we have written our message and submitted it by pressing Enter, the getting of messages proceeds.

Just a friendly reminder, Google is still your friend. The more you Google stuff, the better you get at formulating your search queries of the most accurate search results.

Oh, there is also the [examples directory](examples/), check it out!

## 4.3 Sending a message

Using `urllib2` to perform a `POST` request requires a bit more code compared to when performing a `GET` request. Fortunately, it is quite straight forward.

The key difference is that when performing a `POST` request, we need to have the parameters in a different format. We start by creating a dictionary containing our parameters:

```python
values = {
            'channel': channel,
            'sender': sender,
            'content': content
        }
```

The values then need to be encoded. The encoding is done with `urllib`, not `urllib2`, so remember to import it:

```python
import urllib
values = {...}
encoded_values = urllib.urlencode(values)
```

Now we can create a request:

```python
import urllib
import urllib2
values = {...}
encoded_values = urllib.urlencode(values)
req = urllib2.Request(url, encoded_data)
```

After this, everything is as when doing a `GET` request:

```python

req = urllib2.Request(url, encoded_data)
try:
    resp = urllib2.urlopen(req)
    json_data = resp.read()
except urllib2.HTTPError, e:
    json_data = e.read()
```

Again, we ignore the potential not-OK HTTP status code with our try-catch statement. This is useful with our server, but may not always be very smart. Read more about [HTTP status codes](https://httpstatuses.com)!

**Think about this:** Is it necessary for us to print the server-returned message after sending or does our configuration do that automatically? What benefits do the different methods provide?

Now, just try to implement the message sending functionality. If you break the server, which I doubt you will be able to do, please create open an [issue](https://github.com/Datateknologerna-vid-Abo-Akademi/gulis-chat/issues)!

## 4.4 Conclusion

Okay, I would consider our creation as a functional chat client. Of course, there could be some additional features, such as changing channel or exiting, but for now, it is good enough!

So far we have learned the basics of

* Performing `GET` and `POST` requests
* How to parse JSON in Python
* Simple threads in Python
* Thread locks
* Hopefully more

Here are some suggestions on what features you can add

* /-commands: `/channel`, `/quit` etc.
* Displaying of message time

As always, if you have any questions, remember to look at the [examples](examples/), look at the [issues](ttps://github.com/Datateknologerna-vid-Abo-Akademi/gulis-chat/issues) or ask Google.

In part 5, we start looking at how to make a graphical user interface in Python.
