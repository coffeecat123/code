import turtle
window = turtle.Screen()
a = turtle.Turtle()
a.shape("classic")
a.speed(0)
while True:
    a.pencolor("red")
    print("請輸入3~100的奇數")
    x = int(input())
    a.clear()
    print("開始畫")
    z = 180-360/x/2
    a.begin_fill()
    a.fillcolor("yellow")
    while x != 0:
        a.fd(200)
        a.rt(z)
        x = x-1
    a.end_fill()
    print("畫完了")
    a.pencolor("blue")
    print("請輸入3~100的奇數")
    x = int(input())
    a.clear()
    print("開始畫")
    z = 180-360/x/2
    a.begin_fill()
    a.fillcolor("red")
    while x != 0:
        a.fd(200)
        a.rt(z)
        x = x-1
    a.end_fill()
    print("畫完了")
    a.pencolor("yellow")
    print("請輸入3~100的奇數")
    x = int(input())
    a.clear()
    print("開始畫")
    z = 180-360/x/2
    a.begin_fill()
    a.fillcolor("blue")
    while x != 0:
        a.fd(200)
        a.rt(z)
        x = x-1
    a.end_fill()
    print("畫完了")
