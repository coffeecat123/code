from tkinter import ttk
import tkinter
import tkinter.font as tkFont
root = tkinter.Tk()
f1=tkFont.Font(family="Arial", size=20, weight="bold", slant="italic")
style1 = ttk.Style()
style2 = ttk.Style()
b1 = tkinter.Button(root, text ="circle",cursor="crosshair",font=f1)
b1.pack()
style1.layout("TMenubutton", [
   ("Menubutton.background", None),
   ("Menubutton.button", {"children":
       [("Menubutton.focus", {"children":
           [("Menubutton.padding", {"children":
               [("Menubutton.label",{"side": "left", "expand": 1})]
           })]
       })]
   }),
])
colored_btn = ttk.Button(text="Test", style="C.TButton").pack()
mbtn = ttk.Menubutton(text='Text')
mbtn.pack()
s=ttk.Style()
s.configure('Wild.TButton',
    background='black',
    foreground='white',
    highlightthickness='20',
    font=('Helvetica', 18, 'bold'))
s.map('Wild.TButton',
    foreground=[('disabled', 'yellow'),
            ('pressed', 'red'),
                ('active', 'blue')],
    background=[('disabled', 'magenta'),
                ('pressed', '!focus', 'cyan'),
                ('active', 'pink')],
    highlightcolor=[('focus', 'green'),
                    ('!focus', 'red')],
    relief=[('pressed', 'groove'),
            ('!pressed', 'ridge')])
ttk.Button(text="Test", style="Wild.TButton").pack()
root.mainloop()
