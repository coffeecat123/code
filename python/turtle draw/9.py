from turtle import *
speed(0)
import turtle
s = turtle.Screen()
s.bgcolor('black')
t = clone()
t.color('orange')
t.pensize(3)
t.hideturtle()
def tl():
    t.rt(20)
    a = t.clone()
    for i in range(10):
        a.fd(30)
        a.rt(18)
def tl2():
    t.rt(20)
    a = t.clone()
    for i in range(10):
        a.fd(30)
        a.lt(18)
def tl3():
    a.undo()
    
t.hideturtle()
for i in range(9):
    tl()
    t.color('yellow')
    tl()
    t.color('orange')
t.rt(18)
for i in range(9):
    tl2()
    t.color('yellow')
    tl2()
    t.color('orange')
turtle.done()

    

    

