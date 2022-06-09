from tkinter import *
import tkinter.messagebox
def info_warn_err():
    a=tkinter.messagebox.showinfo("我的标题","我的提示1")
    print(a)
    a=tkinter.messagebox.showwarning("我的标题","我的提示2")
    print(a)
    a=tkinter.messagebox.showerror("我的标题", "我的提示3")
    print(a)
def func2():
    a=tkinter.messagebox.askyesno("我的标题","我的提示1")
    print(a)
    a=tkinter.messagebox.askokcancel("我的标题","我的提示2")
    print(a)
    a=tkinter.messagebox.askquestion("www.tianqiweiqi.com","我的提示3")
    print(a)
    a=tkinter.messagebox.askretrycancel("我的标题","我的提示4")
    print(a)
    a=tkinter.messagebox.askyesnocancel("我的标题","我的提示5")
    print(a)
    #这里用作演示如何使用对话框
    if tkinter.messagebox.askyesno("我的标题", "确认关闭窗口吗!"):
        root.destroy()
root=Tk()
btn=Button(root,text="信息、警告、错误消息框",command=info_warn_err)
btn1=Button(root,text="对话框",command=func2)
btn.pack()
btn1.pack()
root.mainloop()
