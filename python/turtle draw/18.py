import turtle as a
import random as r
s = a.Screen()
s.bgcolor('black')
a.speed(0)
def abc(x,y):
    global e
    a.up()
    a.goto(r.randint(-300,300),r.randint(-300,300))
    a.rt(r.randint(0,360))
    a.down()
    a.begin_fill()
    a.fillcolor(e[r.randint(0,2)])
    for i in range(x):
        a.fd(y)
        a.rt(180-180/x)
    a.end_fill()
while True:
    e = ['red','yellow','blue']
    c = r.randint(5,20)
    while c%2 !=1:
        c = r.randint(5,20)
    abc(c,r.randint(50,100))
