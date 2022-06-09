import time
import turtle
window = turtle.Screen()
a = turtle.Turtle()
a.shape("classic")
a.pensize(3)
a.speed(0)
x = 5
while True:
    a.pencolor("red")
    a.clear()
    print("開始畫")
    z = 180-360/x/2
    a.begin_fill()
    a.fillcolor("yellow")
    for i in range(int(x)):
        a.fd(300)
        a.rt(z)
    a.end_fill()
    print("畫完了")
    x = x +2
    time.sleep(0.5)
