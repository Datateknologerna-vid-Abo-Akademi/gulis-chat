# gulis-chat

Server for the gulis-chat course. The running requires [Docker](https://docker.com) or [Go](https://golang.org) to be installed.

[localhost:8080](http://localhost:8080)

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
docker run --rm -p 8080:8080 -v "$(pwd)"/db:/root/db -t gulis-chat/server
```

Starts a container from the image built.

**--rm** removes the container when stopped

**-p** connects host and container ports

**-v** links host and container volumes, this way the DB file exists on host machine

**-t** specifies which image to start based on tag

### Stop

Exit the running container with **Ctrl+C**

Find the container ID

```sh
docker ps
```

Stop the process

```sh
docker stop <containerID>
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