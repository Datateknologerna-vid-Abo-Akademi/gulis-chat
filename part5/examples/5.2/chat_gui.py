from Tkinter import *


class ChatGUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)    # Initialize the frame
        self.pack()                     # Pack everything


root = Tk()     # Init Tkinter
root.title("Gulis Chat")    # Set window title
app = ChatGUI(master=root)  # Create our frame
app.mainloop()  # Run

# If the app doesn't terminate, let's destroy it
try:
    root.destroy()  # Destroy the frame
except tkinter.TclError:
    pass    # The frame has probably already exited
