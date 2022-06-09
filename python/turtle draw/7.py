import turtle as a
a.speed(0)
while True:
    x = 240
    y = 0
    while True:
        while y<=0:
            y = int(input("幾圈(240的因數)"))
        if 240%y == 0:
            break
        y = -1
    a.up()
    a.rt(90)
    a.fd(x*7/8)
    a.lt(90)
    a.hideturtle()
    a.clear()
    while x != 0:
        a.down()
        a.circle(x)
        x = x-y
        a.up()
        a.lt(90)
        a.fd(y)
        a.rt(90)
