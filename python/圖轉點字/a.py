from PIL import Image
import os
import random as r
import pyperclip as p
import sys
def add(q):
    global c
    return (c[q][0]+c[q][1]+c[q][2])/3
def open_as_rgb(path, bg=(255, 255, 255)):
    im = Image.open(path)
    if im.mode == "RGBA":
        background = Image.new("RGB", im.size, bg)
        background.paste(im, mask=im.split()[3])
        return background
    return im.convert("RGB")
a='\
⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏\
⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟\
⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯\
⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿\
⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏\
⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟\
⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯\
⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿\
⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏\
⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟\
⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯\
⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿\
⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏\
⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟\
⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯\
⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿'
a1='⠁⠂⠄⠈⠐⠠⡀⢀'
file=sys.argv[1]
im = im = open_as_rgb(file, bg=(255,255,255))
c = list(im.getdata())
c1=[]
for i in range(len(c)):
    c1.append((c[i][0],c[i][1],c[i][2]))
c=c1
x,y=im.size
x1=100#行
y1=100#列
z=''
k=128
for i in range(0,y,4):
    for j in range(0,x,2):
        s=0
        if(add((i+0)*x+j+0)<=k):
            s+=1
        if(add((i+1)*x+j+0)<=k):
            s+=2
        if(add((i+2)*x+j+0)<=k):
            s+=4
        if(add((i+0)*x+j+1)<=k):
            s+=8
        if(add((i+1)*x+j+1)<=k):
            s+=16
        if(add((i+2)*x+j+1)<=k):
            s+=32
        if(add((i+3)*x+j+0)<=k):
            s+=64
        if(add((i+3)*x+j+1)<=k):
            s+=128
        z1=a[s]
        if(z1==a[0]):
            #z+=r.choice(a1)
            z+=z1
        else:
            z+=z1
        j+=2
    z+='\n'
    i+=4
print(z)
p.copy(z)
