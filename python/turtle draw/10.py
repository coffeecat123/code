from turtle import *
speed(0)
import turtle
s = turtle.Screen()
s.bgcolor('black')
t = clone()
t.color('white')
t.pensize(3)
t.hideturtle()
x = 100
def tl():
    a = t.clone()
    for i in range(9):
        a.fd(30)
        a.rt(20)
    t.rt(20)
def tl2():
    a = t.clone()
    for i in range(9):
        a.fd(30)
        a.lt(20)
    t.lt(20)
for i in range(18):
    tl()
t.rt(18)
for i in range(18):
    tl2()

t.color('black')
t.pensize(3)
for i in range(18):
    tl()
t.rt(9)
for i in range(18):
    tl2()
turtle.done()
