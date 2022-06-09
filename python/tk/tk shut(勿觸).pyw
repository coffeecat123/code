import tkinter as tk
import threading
import tkinter.messagebox
import os
import time
def kf():
    global i
    for d in range(i):
        time.sleep(1)
        i-=1
w=tk.Tk()
w.withdraw()
i=10
t=threading.Thread(target=kf)
t.start()
while i>0:
    tk.messagebox.showerror('電腦中毒',
        '電腦中毒\n將在一分鐘後關機\n剩'+
            str(i)+'秒')
t.join()
w.destroy()
os.system('pause')
