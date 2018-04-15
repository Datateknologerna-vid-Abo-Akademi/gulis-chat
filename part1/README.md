# Part 1

This is the first part of the gulis-chat course. If you haven't set up your development environment yet, do it now.

If everything is set up, let's get started!

## 1.1 Exploring the API

Let's start by exploring the API of our server.

Visit [37.59.100.46:10080](http://37.59.100.46:10080) and take a look at the API reference.

### Endpoints

We can see that the server has three API endpoints: `/get`, `/past` and `/send`.

The endpoint accept different request methods, namely `GET` and `POST`. 
This means we must remember these when we do requests from our application.

### Objects

From the API reference we see that the server returns two kinds of objects.
Both are of the [JSON format](http://json.org).

`message` is a the messages sent to the server.

`error` is simply an error message.

### 1.2.1 Testing the API - Send

Open the Insomnia REST client. If you still don't have it, [install it](https://insomnia.rest).

In Insomnia, create a new folder, let's call it `gulis-chat`.

Add a request inside the folder, name it `send`, select `POST` as the method and select `Form` as the body.

In the upper bar, add the URL `http://37.59.100.46:10080/send`.

Now, before we fill anything in the form, let's try sending an empty request body to the server.
Click the send button next to the URL field to see what happens.

We should receive this:

```json
{
	"error": "Channel, sender or content empty"
}
```

This is what the `error` object from the API reference looks like.

Next, let's add the following name value pairs to the form in Insomnia:

| name      | value         |
| :-------: | :-----------: |
| channel   | test          |
| sender    | YourName      |
| content   | Hello World   |

Click send.

This time you should get something like this:

````json
{
	"id": 5,
	"channel": "test",
	"sender": "Otto",
	"content": "Hello World",
	"time": "2018-04-15T19:33:56Z"
}
````

### 1.2.2 Testing the API - Get and Past

The `/get` and `/past` endpoints are accessible with a `GET` method.
We will therefore add two new requests to our `gulis-chat` folder in Insomnia.

Name them `get` and `past` and let the method be `GET`.

For `get`, the URL is `http://37.59.100.46:10080/get`.

For `past`, the URL is `http://37.59.100.46:10080/past`.

Becouse these are the `GET` methods, we will not be sending a form. Rather, the parameters are added to the URL.
To see how this works, select the Query tab in Insomnia. 

In the query tab, you can fill in values the same way we did with the `send` request in the form.

Try adding parameters accordingly to the API reference!

Remember that `channel` is a required parameter in all endpoints.

If you have any questions, feel free to ask your tutors or see if there are any open [issues](https://github.com/Datateknologerna-vid-Abo-Akademi/gulis-chat/issues).

### 1.3 Conclusion

Hopefully you have some understanding of how the API works and what it returns.

In part 2, we will create a simple Python script for communicating with the server.

#### Something to think about

What are the pros and cons of this server, where anyone can send messages and choose their own username without registration?