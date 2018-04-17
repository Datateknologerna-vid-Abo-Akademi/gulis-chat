# gulis-chat

Server for the gulis-chat course. The running requires [Docker](https://docker.com) or [Go](https://golang.org) to be installed.

[localhost:8080](http://localhost:10080)

## Docker

Run these commands in the `server` directory!

### Build

```sh
docker build -t gulis-chat/server . -f docker/Dockerfile
```

Builds the docker image.

**-t** specifies the tag

**.** specifies what folder to execute in

**-f** specifies the Docker file to use

### Run

Use absolute path with `-v`. This command works on Linux and macOS.

```sh
docker run --rm -p 10080:10080 -v "$(pwd)"/db:/root/db -it gulis-chat/server
```

Starts a container from the image built.

**--rm** removes the container when stopped

**-p** connects host and container ports

**-v** links host and container volumes, this way the DB file exists on host machine

**-it** allocate a tty

### Stop

Exit the running container with **Ctrl+C**

Find the container ID

```sh
docker ps
```

Stop the process

```sh
docker stop [containerID]
```

## Go

Make sure your GO_ environmental variables are correct and that gcc is installed.

Run these commands in the `server` directory!

### Run

```sh
go run server.go
```

### Build and run

```sh
go build server.go -o server; ./server
```

## Deployment with docker

Run these from the `server` directory!

### On local machine

Create a alpine image:

```sh
docker build -t gulis-chat/server . -f docker/Dockerfile.multi
```

Save the image:

```sh
docker save gulis-chat/server > gulis-chat-server.tar
```

Copy the `gulis-chat-server.tar` file to the server.

### On server

Locate the `gulis-chat-server.tar` and load to docker:

```sh
docker load -i gulis-chat-server.tar
```

**Save and move to server the haxx way:**

```sh
docker save gulis-chat/server | bzip2 | ssh user@host 'bunzip2 | docker load'
```

Make sure there is a directory for the DB, otherwise, make one.

Run the container:

```sh
docker run -d -v /absolute/path/to/db/direcrory:/root/db -p 10080:10080 gulis-chat/server
```

Make sure the port is open!