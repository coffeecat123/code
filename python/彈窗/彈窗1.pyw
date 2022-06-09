import tkinter as tk
import random
import threading
import time
def dow():
    window = tk.Tk()
    width=window.winfo_screenwidth()
    height=window.winfo_screenheight()
    a=random.randrange(0,width)
    b=random.randrange(0,height)
    window.title('新年愉快')
    window.geometry("200x50"+"+"+str(a)+"+"+str(b))
    tk.Label(window,
        text='happybirthday)！',    # 标签的文字
        bg='Red',     # 背景颜色
        font=('楷體', 17),     # 字体和字体大小
        width=20, height=2  # 标签长宽
        ).pack()    # 固定窗口位置
    window.mainloop()
threads = []
for i in range(1000):#需要的弹框数量
    t = threading.Thread(target=dow)
    threads.append(t)
    #time.sleep(0.025)
    threads[i].start()
