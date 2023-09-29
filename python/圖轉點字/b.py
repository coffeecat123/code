from PIL import Image
import os
import random as r
import pyperclip as p
import sys
def add(q):
    global c
    return (c[q][0]+c[q][1]+c[q][2])/3
#1,8,28,56,70,56,28,8,1
a='⠀⡐⡑⢙⢇⢳⣗⣽⣿'
a1='⠁⠂⠄⠈⠐⠠⡀⢀'
file=sys.argv[1]
im = Image.open(file)
c = list(im.getdata())
c1=[]
for i in range(len(c)):
    c1.append((c[i][0],c[i][1],c[i][2]))
c=c1
x,y=im.size
z=''
i=0
while(i<y):
    j=0
    while(j<x):
        z1=a[len(a)-1-int(add(i*x+j)/255*(len(a)-1))]
        if(z1==a[0]):
            z+=r.choice(a1)
        else:
            z+=z1
        j+=1
    z+='\n'
    i+=2
print(z)
p.copy(z)
