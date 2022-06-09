import tkinter as a
import turtle as tl
count = 0
window = a.Tk()
def abc():
    global count
    count = count+1
    button.config(text=str(count))
def changeString():
    stringToCopy = entry.get()
button = a.Button(window, text='點我',command = abc)
button.pack()
window.mainloop()
