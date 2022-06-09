import turtle as t
y = 3
t.speed(0)
while True:
    z = 1#可調
    x = z
    t.down()
    for i in range(1000//z//y):
        for i in range(y//2):    
            t.fd(x)
            t.lt(360/y-1)
        x = x+z
    y = y+1
    t.up()
    t.home()
    t.clear()
    
