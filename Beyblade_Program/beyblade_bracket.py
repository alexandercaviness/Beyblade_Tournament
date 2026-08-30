import tkinter
from tkinter import *

def cancel_window():
    root.destroy()


root = tkinter.Tk()

root.geometry("750x500")

image_path= PhotoImage(file="images/beyblade_emblem.png")
my_label = Label(root,image= image_path)
my_label.place(x=0, y=0, relwidth = 1, relheight=1)
cancel_bttn= tkinter.Button(root, text= "Cancel", command = cancel_window)

cancel_bttn.pack()



root.mainloop()