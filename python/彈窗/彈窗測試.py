import tkinter as tk
import random
import threading
import tkinter.messagebox
import time
def dow():
    tk.messagebox.showerror('電腦中毒',
        '電腦中毒\n將在一分鐘後關機\n剩'+
            'abc'+'秒')
threads = []
i=20
z=i
while i>0:
    t=threading.Thread(target=dow)
    threads.append(t)
    threads[z-i].start()
    i-=1
