import turtle as a
a.tracer(False)
a.hideturtle()
s = a.Screen()
s.bgcolor('black')
while True:
    x = int(input("幾邊形"))
    b = x
    z = int(input("重複幾次(1~360)"))
    d = z
    a.clear()
    a.begin_fill()
    a.fillcolor('yellow')
    while z != 0:
        y = x
        while y != 0:
            a.fd(700/x)
            a.rt(360/b)
            y = y-1
        a.rt(360/d)
        z = z-1
    a.end_fill()
    a.update()
    
