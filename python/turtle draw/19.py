from tkinter import *
tk = Tk()
tk.geometry('500x500+0+0')
a = Canvas(tk,width=200,height=300)
a.pack()
a.create_line(0,0,200,100,width=0.1)
a.create_line(0,100,200,0,fill='red',dash=(4,4))
tk.mainloop()
