from Tkinter import *


class ChatGUI(Frame):

    def set_name(self):
        return

    def set_channel(self):
        return

    def send_message(self):
        return

    def create_widgets(self):
        self.MENU = Frame(self)

        self.BTN_CHANNEL = Button(self.MENU, text="Channel", command=self.set_channel)
        self.BTN_CHANNEL.pack(side=LEFT, fill=X)

        self.BTN_NAME = Button(self.MENU, text="Name", command=self.set_name)
        self.BTN_NAME.pack(side=LEFT, fill=X)

        self.MENU.pack(fill=X)

        self.MESSAGE_VIEW = Frame(self, borderwidth=2, relief=SUNKEN)

        self.MESSAGES = Text(self.MESSAGE_VIEW, height=20, width=60, foreground='black')
        self.MESSAGES.pack(side=LEFT, fill=Y)

        self.SCROLLBAR = Scrollbar(self.MESSAGE_VIEW)
        self.SCROLLBAR.pack(side=RIGHT, fill=Y)

        self.SCROLLBAR.config(command=self.MESSAGES.yview)
        self.MESSAGES.config(yscrollcommand=self.SCROLLBAR.set)
        self.MESSAGES.bind("<Key>", lambda e: "break")

        self.MESSAGE_VIEW.pack()

        self.WRITE_VIEW = Frame(self)

        self.WRITE = Entry(self.WRITE_VIEW, width=40)
        self.WRITE.pack(side=LEFT, fill=Y)

        self.BTN_SEND = Button(self.WRITE_VIEW, text="Send", command=self.send_message)
        self.BTN_SEND.pack(side=RIGHT, fill=X)

        self.WRITE_VIEW.pack()

    def __init__(self, master):
        Frame.__init__(self, master)    # Initialize the frame
        self.create_widgets()           # Add all our widgets
        self.master.config(menu=self.MENU)  # Add a menubar
        self.pack()                     # Pack everything


root = Tk()
root.title("Gulis Chat")
app = ChatGUI(master=root)
app.mainloop()

# If the app doesn't terminate, let's destroy it
try:
    root.destroy()
except tkinter.TclError:
    pass
