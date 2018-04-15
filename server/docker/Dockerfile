FROM golang:1.10-alpine

RUN apk add --no-cache --update gcc musl-dev git mercurial

ENV SRC_DIR=/go/src/github.com/Datateknologerna-vid-Abo-Akademi/gulis-chat/server/

WORKDIR /root

ADD . $SRC_DIR

RUN cd $SRC_DIR; go get -v ./...

RUN cd $SRC_DIR; go build -o server; cp server /root/

RUN cd $SRC_DIR; cp -R static /root/

RUN mkdir /root/db

VOLUME /root/db

EXPOSE 8080

ENTRYPOINT ["./server"]