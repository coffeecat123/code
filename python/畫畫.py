import turtle

def onmove(self, fun, add=None):
    if fun is None:
        self.cv.unbind('<B1-Motion>')
    else:
        def eventfun(event):
            fun(self.cv.canvasx(event.x) / self.xscale, -self.cv.canvasy(event.y) / self.yscale)
        self.cv.bind('<B1-Motion>', eventfun, add)
def goto_handler(x, y):
    onmove(turtle.Screen(), None)  # avoid overlapping events
    turtle.setheading(turtle.towards(x, y))
    turtle.goto(x, y)
    onmove(turtle.Screen(), goto_handler)
onmove(turtle.Screen(), goto_handler)
turtle.speed(0)
turtle.mainloop()
