import tkinter as tk
def ats():
    print(1)
class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
    def createWidgets(self):
        #按鈕
        self.button = tk.Button(self,command=ats)
        self.button["text"] = "demo"
        self.button.grid(row=0, column=0, sticky=tk.N+tk.W)
        #核取按鈕
        self.checkbutton1=tk.Checkbutton(self)
        self.checkbutton1["text"]="demo1"
        self.checkbutton1.grid(row=0, column=1,sticky=tk.N+tk.W)
        self.checkbutton2=tk.Checkbutton(self)
        self.checkbutton2["text"]="demo2"
        self.checkbutton2.grid(row=1, column=1,sticky=tk.N+tk.W)
        #文字輸入欄
        self.entry = tk.Entry(self)
        self.entry.grid(row=5, column=1, sticky=tk.N+tk.W)
        #文字標籤
        self.label = tk.Label(self)
        self.label["text"] = "demo"
        self.label.grid(row=1, column=0, sticky=tk.N+tk.W)
        #下拉式的選項選單
        self.optionList=("Python","Java","Swift")
        self.v=tk.StringVar()
        self.v.set("demo")
        self.optionmenu=tk.OptionMenu(self,self.v,*self.optionList)
        self.optionmenu.grid(row=3,column=1,sticky=tk.N+tk.W)
        #單選按鈕
        self.radiobutton = tk.Radiobutton(self)
        self.radiobutton["text"]='demo'
        self.radiobutton.grid(row=4,column=0,sticky=tk.N+tk.W)
        #微調器
        self.spinbox=tk.Spinbox(self,from_=0,to=10)
        self.spinbox.grid(row=4,column=1,sticky=tk.N+tk.W)
        #文字方塊
        self.text=tk.Text(self)
        self.text["height"]=5
        self.text["width"]=10
        self.text.grid(row=3,column=0,sticky=tk.N+tk.W)
        #拉桿
        self.scale = tk.Scale(self)
        self.scale.grid(row=2,column=0,sticky=tk.N+tk.W)
        #列表選單
        self.listbox = tk.Listbox(self)
        self.listbox["height"] = 5
        self.listbox.insert(1, "Python")
        self.listbox.insert(2, "Java")
        self.listbox.insert(3, "Swift")
        self.listbox.insert(4, "JavaScript")
        self.listbox.insert(5, "C")
        self.listbox.grid(row=2, column=1, sticky=tk.N+tk.W)

w = tk.Tk()
q = Application(w)
w.geometry('300x200')
w.title("tkinter")
w.configure(background='#FF0000')
a = tk.Menu(w)
b=tk.Menu(a,tearoff=0)
c=tk.Menu(a,tearoff=0)
b.add_command(label="Open")
b.add_command(label="Save")
b.add_command(label="Exit")
for i in range(26):
    c.add_command(label=chr(i+65))
a.add_cascade(label="File", menu=b)
a.add_cascade(label="字母", menu=c)
w.config(menu=a)
w.mainloop()
'''
Frame	視窗。
Label	文字標籤。
Button	按鈕。
Canvas	可以用來繪圖、文字等都可以，像我就會來拿放圖片。
Checkbutton	核取按鈕。
Entry	文字輸入欄。
Listbox	列表選單。
Menu	選單列的下拉式選單。
LabelFrame	文字標籤視窗。
MenuButton	選單的選項。
Message	類似 Label ，可多行。
OptionMenu	下拉式的選項選單。
PaneWindow	類似 Frame ，可包含其他視窗元件。
Radiobutton	單選按鈕。
Scale	拉桿。
Scrollbar	捲軸。
Spinbox	微調器
Text	文字方塊。
Toplevel	新增視窗。
'''
