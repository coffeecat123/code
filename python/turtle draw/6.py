import turtle 
from random import randint
a = turtle.Turtle()
s = turtle.Screen()
s.bgcolor('black')
a.hideturtle()
a.speed(0)
a.down()
a.color("light blue")
for u in range(100):
    a.goto(randint(-1000,1000),randint(-1000,1000))
    a.pensize(randint(1,5))
