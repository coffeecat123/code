import tkinter as a
import turtle as tl
tl.speed(0)
window = a.Tk()
def abc():
    for i in range(20):
        tl.rt(83)
        tl.fd(100)
button = a.Button(window, text='點我',command = abc)
button.pack()
window.mainloop()
