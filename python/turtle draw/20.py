import turtle as t
#t.speed(0)
t.tracer(0)
t.goto(0,200)
t.clear()
y=10
x=700
a=3
for j in range(a):
    for i in range(x):
        t.fd(y)
        t.rt(3)
        y*=0.99
    t.rt(180)
    t.rt(360/a)
    for i in range(x):
        t.lt(3)
        y/=0.99
        t.fd(y)
    t.rt(180)
#t.update()
