from Tkinter import *


def update_label():
    value = str(entry.get())
    label_value.set(value)
    entry.delete(0, END)


root = Tk()
app = Frame(master=root)

label_value = StringVar()
label_value.set("Hello world!")

label = Label(master=app, textvariable=label_value)
label.pack()

entry = Entry(master=app)
entry.pack()

button = Button(master=app, text="Update", command=update_label)
button.pack()

app.pack()
app.mainloop()
