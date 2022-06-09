import turtle as a
a.hideturtle()
a.speed(0)
a.color('black')
def tl():
    for i in range(10):
        a.fd(1)
        a.rt(1)
def tl2():
    a.rt(90)
    for i in range(10):
        a.fd(1)
        a.rt(1)
    a.lt(90)
for i in range(18):
    tl()
    tl2()
a.up()
a.home()
a.bk(40)
a.rt(90)
a.fd(30)
a.color('red')
a.pensize(5)
a.write('good!')
