import tkinter as tk
import tkinter.messagebox
import os
w=tk.Tk()
for i in range(60):
    tk.messagebox.showerror('電腦中毒',
        '電腦中毒\n將在一分鐘後關機\n剩'+
            str(60-i)+'秒')
w.destroy()
os.system('pause')
