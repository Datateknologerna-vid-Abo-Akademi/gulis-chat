package main

import (
	"fmt"
	"log"
	"path"
	"strings"
	"html"
	"time"
	"net/http"
	"encoding/json"
	"github.com/gorilla/mux"
	"github.com/jmoiron/sqlx"
	_ "github.com/mattn/go-sqlite3"
	"strconv"
	"math"
)

const (
	port   = "10080"
	DBPath = "db"
	DBFile = "chat.db"
)

func main() {

	initDB()

	m := mux.NewRouter()

	m.HandleFunc("/send", handleSend).Methods(http.MethodPost)
	m.HandleFunc("/get", handleGet).Methods(http.MethodGet)
	m.HandleFunc("/past", handlePast).Methods(http.MethodGet)

	staticFileHandler := http.StripPrefix("/", http.FileServer(http.Dir("static/")))
	m.PathPrefix("/").Handler(staticFileHandler)

	http.Handle("/", m)

	fmt.Println("Server running on port", port)

	log.Fatal(http.ListenAndServe(":"+port, nil))
}

func handleSend(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()

	channel := formValue(r, "channel")
	sender := formValue(r, "sender")
	content := formValue(r, "content")

	if len(channel) == 0 || len(sender) == 0 || len(content) == 0 {
		sendErrorJSON(w, "Channel, sender or content empty", http.StatusBadRequest)
		return
	}

	msg := createMessage(channel, sender, content)
	err := msg.storeMessage()
	if err != nil {
		log.Println(err)
		sendErrorJSON(w, "Server failed to save message", http.StatusInternalServerError)
		return
	}

	sendJSON(w, msg, http.StatusOK)
}

func handleGet(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()

	channel := formValue(r, "channel")
	lastStr := formValue(r, "last")

	var last int64 = 0

	if len(channel) == 0 {
		sendErrorJSON(w, "Channel empty", http.StatusBadRequest)
	}

	if len(lastStr) != 0 {
		l, err := strconv.ParseInt(lastStr, 10, 64)
		if err != nil {
			sendErrorJSON(w, "Last must be of type int64", http.StatusBadRequest)
			return
		}
		last = l
	}

	msgs, err := getNewMessages(channel, last)
	if err != nil {
		log.Println(err)
		sendErrorJSON(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	sendJSON(w, msgs, http.StatusOK)
}

func handlePast(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()

	channel := formValue(r, "channel")
	countStr := formValue(r, "count")
	beforeStr := formValue(r, "before")

	count := 100
	var before int64 = math.MaxInt64

	if len(channel) == 0 {
		sendErrorJSON(w, "Channel empty", http.StatusBadRequest)
	}

	if len(countStr) != 0 {
		i, err := strconv.Atoi(countStr)
		if err != nil {
			sendErrorJSON(w, "Count must be of type int", http.StatusBadRequest)
			return
		}
		count = i
	}

	if len(beforeStr) != 0 {
		i, err := strconv.ParseInt(beforeStr, 10, 64)
		if err != nil {
			sendErrorJSON(w, "Before must be of type int64", http.StatusBadRequest)
			return
		}
		before = i
	}

	msgs, err := getOldMessages(channel, before, count)
	if err != nil {
		log.Println(err)
		sendErrorJSON(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	sendJSON(w, msgs, http.StatusOK)
}

func sendJSON(w http.ResponseWriter, item interface{}, code int) error {
	data, err := json.Marshal(item)
	if err != nil {
		return err
	}

	w.Header().Add("Content-type", "json")
	w.WriteHeader(code)
	_, err = w.Write(data)
	return err
}

func sendErrorJSON(w http.ResponseWriter, err string, code int) error {
	type eroor struct {
		Error string `json:"error"`
	}
	return sendJSON(w, eroor{err}, code)
}

func formValue(r *http.Request, key string) string {
	return html.EscapeString(strings.TrimSpace(r.FormValue(key)))
}

func openDB() (*sqlx.DB, error) {
	db, err := sqlx.Open("sqlite3", path.Join(DBPath, DBFile))
	return db, err
}

func initDB() {
	db, err := openDB()
	defer db.Close()

	if err != nil {
		log.Fatal("Could not open DB ", err)
	}

	qry := `
		CREATE TABLE IF NOT EXISTS chats (
			id INTEGER UNIQUE NOT NULL PRIMARY KEY,
			channel INTEGER NOT NULL,
			sender TEXT NOT NULL,
			content TEXT NOT NULL,
			time DATETIME NOT NULL
			);`

	_, err = db.Exec(qry)

	if err != nil {
		log.Fatal("Could not create table in DB", err)
	}
}

type message struct {
	ID      int64  `json:"id" db:"id"`
	Channel string `json:"channel" db:"channel"`
	Sender  string `json:"sender" db:"sender"`
	Content string `json:"content" db:"content"`
	Time    string `json:"time" db:"time"`
}

func createMessage(channel, sender, content string) (msg *message) {
	return &message{
		Channel: channel,
		Sender:  sender,
		Content: content,
		Time:    time.Now().Format(time.RFC3339),
	}
}

func (msg *message) storeMessage() (err error) {
	qry := `INSERT INTO chats (channel, sender, content, time) VALUES (?, ?, ?, ?)`

	db, err := openDB()
	defer db.Close()
	if err != nil {
		return
	}

	statement, err := db.Prepare(qry)
	if err != nil {
		return
	}

	res, err := statement.Exec(msg.Channel, msg.Sender, msg.Content, msg.Time)
	if err != nil {
		return
	}

	id, err := res.LastInsertId()
	if err != nil {
		return
	}

	msg.ID = id

	return
}

func getNewMessages(channel string, last int64) (*[]message, error) {
	var messages []message

	db, err := openDB()
	defer db.Close()
	if err != nil {
		return &messages, err
	}

	qry := `SELECT * FROM chats WHERE channel=? AND id>?`

	return &messages, db.Select(&messages, qry, channel, last)
}

func getOldMessages(channel string, before int64, count int) (*[]message, error) {
	var messages []message

	db, err := openDB()
	defer db.Close()
	if err != nil {
		return &messages, err
	}

	qry := `SELECT * FROM (SELECT * FROM chats WHERE channel=? AND id<? ORDER BY id DESC LIMIT ?) ORDER BY id ASC`

	return &messages, db.Select(&messages, qry, channel, before, count)
}
