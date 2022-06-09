import tkinter as tk
window = tk.Tk()
window.title('my window')
window.geometry('200x200')
l = tk.Label(window, bg='yellow', width=20, text='0')
l.pack()
def print_selection(v):
    l.config(text='you have selected ' + v)
s=tk.Scale(window, label='try me',
           from_=0, to=10,
           orient=tk.HORIZONTAL,
           length=200, showvalue=1,
           tickinterval=2,resolution=1,
           command=print_selection)
s.pack()
window.mainloop()
