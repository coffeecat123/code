import turtle as t
t.speed(5)
y = 0.1
x = y
t.fillcolor('red')
for i in range(30):
    t.circle(y*10,180)
    y = y+1
    t.lt(90)
    t.fd(y*5)
    t.bk(y*5)
    t.rt(90)
    t.end_fill()
while True:
    y = 0.1
    for i in range(100):
        for i in range(180):
            t.fd(x)
            t.lt(1)
        x = x+y
