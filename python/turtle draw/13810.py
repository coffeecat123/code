from tkinter import *
tk = Tk()
def ab(e):
    if e.num == 1:
        mouse_chick_type='lt'
    elif e.num == 3:
        mouse_chick_type='rt'
    else:
        mouse_chick_type='other'
    print(mouse_chick_type,e.x,e.y)

tk.bind('<Button-1>',ab)
tk.bind('<Button-3>',ab)
tk.mainloop()
