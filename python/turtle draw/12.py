import turtle as a
x = 0.01
#a.speed(0)
a.tracer(0)
for i in range(18000):
    a.fd(x)
    a.rt(1/100)
    
print(36000*x/a.ycor()*-1)

for i in range(3600):
    a.fd(x)
    a.rt(1/10)
while True:
    a.ht()

