import tkinter as tk
window = tk.Tk()
def sliderUpdate(source):
    red = redSlider.get()
    green = greenSlider.get()
    blue = blueSlider.get()
    color = '#%02x%02x%02x' % (red, green, blue)
    canvas.config(bg=color)

redSlider = tk.Scale(window, from_=0, to=255, command=sliderUpdate)
greenSlider = tk.Scale(window, from_=0, to=255, command=sliderUpdate)
blueSlider = tk.Scale(window, from_=0, to=255, command=sliderUpdate)

canvas = tk.Canvas(window, width=200, height=200)

redSlider.grid(row=1, column=3)
greenSlider.grid(row=1, column=2)
blueSlider.grid(row=1, column=1)

canvas.grid(row=2, column=1, columnspan=3)
tk.mainloop()
