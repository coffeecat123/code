from PIL import Image
import random as r
print('請把要重複的圖片檔名改成1.jpg')
try:
    x=int(input('長:'))
    y=int(input('寬:'))
    file='1.jpg'
    im = Image.open(file)
    image=im.getdata()
    xa,ya=image.size
    c=[]
    for i in range(8):
        c.append([0]*(xa*ya))
    q=list(im.getdata())
    for i in range(ya):
        for j in range(xa):
            c[0][i*xa+j]=q[i*xa+j]
    for i in range(ya):
        for j in range(xa):
            c[1][i*xa+j]=q[i+j*ya]
    for i in range(ya):
        for j in range(xa):
            c[2][i*xa+j]=q[(ya-1-i)*xa+j]
    for i in range(ya):
        for j in range(xa):
            c[3][i*xa+j]=q[(ya-1-i)+j*ya]
    for i in range(ya):
        for j in range(xa):
            c[4][i*xa+j]=q[i*xa+(xa-1-j)]
    for i in range(ya):
        for j in range(xa):
            c[5][i*xa+j]=q[i+(xa-1-j)*ya]
    for i in range(ya):
        for j in range(xa):
            c[6][i*xa+j]=q[(ya-1-i)*xa+(xa-1-j)]
    for i in range(ya):
        for j in range(xa):
            c[7][i*xa+j]=q[(ya-1-i)+(xa-1-j)*ya]
    s=[0]*ya*xa*x*y
    d=[0,2,4,6]
    e=[]
    for i in range(x*y):
        e.append(r.choice(d))
    for i in range(ya*y):
        for j in range(xa*x):
            '''
            if(i%ya==0 and j%xa==0):
                print(i//ya*x+j//xa)
            '''
            s[i*x*xa+j]=c[e[i//ya*x+j//xa]][i%ya*xa+j%xa]
    image_out = Image.new(image.mode,(xa*x,ya*y))
    image_out.putdata(s)
    image_out.save('2.png')
    #print(e)
except:
    pass
