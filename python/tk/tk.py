import tkinter as tk
import tkinter.colorchooser as cc
class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
    def createWidgets(self):
        #拉桿
        self.scale = tk.Scale(self)
        self.scale.grid(row=7, column=0, sticky=tk.N+tk.W)
def CallColor():
    Color=cc.askcolor()
    print(Color)
w = tk.Tk()
tk.Button(w,text="Select Color",command=CallColor).grid()
q = Application(w)
w.geometry('300x200')
w.title("tkinter")
w.configure(background='white')
w.mainloop()
print(q.scale)
