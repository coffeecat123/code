import tkinter as tk
import tkinter.messagebox
import threading
from tkinter import ttk
import time
#計時
def kf():
    time.sleep(1)
#messagebox
def hit_me():
    tk.messagebox.showinfo(title='Hi',message='hahahaha')# return 'ok'
    tk.messagebox.showwarning(title='Hi',message='nononono')# return 'ok'
    tk.messagebox.showerror(title='Hi',message='nonono!')# return 'ok'
    print(tk.messagebox.askokcancel(title='Hi',message='hahahaha'))# return True, False
    print(tk.messagebox.askretrycancel(title='Hi',message='hahahaha'))# return True, False
    print(tk.messagebox.askyesnocancel(title='Hi',message='haha'))# return, True, False, None
    print(tk.messagebox.askquestion(title='Hi',message='hahahaha'))# return 'yes' , 'no'
    print(tk.messagebox.askyesno(title='Hi',message='hahahaha'))# return True, False
#更改文字標籤
def print_selection1(v):
    lk.config(text='you have selected ' + v)
#
'''
def print_selection2():
    value = lb.get(lb.curselection())
    var1.set(value)
    '''
d=threading.Thread(target=kf)
d.start()#執行子程式
d.join()#等d的函式結束
window = tk.Tk()#視窗
window.title('my window')#標題
window.geometry('200x500+0+0')#大小加位置
#文字標籤
lk=tk.Label(window, bg='yellow', width=20, text='0')
lk.pack()
#拉桿
s=tk.Scale(window,label='try me',
           from_=5, to=11,
           orient=tk.HORIZONTAL,
           length=200, showvalue=1,
           tickinterval=2,resolution=0.1,
           command=print_selection1)
s.pack()
#按鈕
ttk.Button(window,text='hit me',command=hit_me).pack()
tk.Button(window,text='hit me',command=hit_me).pack()
#輸入框
e = tk.Entry(window, show=None)
e.pack()
#文字框
t = tk.Text(window, height=5)  
t.pack()
#下拉選單
var1 = tk.StringVar()
var2 = tk.StringVar()
var2.set((11,22,33,44))
#主程式循環
window.mainloop()
