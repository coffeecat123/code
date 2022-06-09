from PIL import Image
print('請把要重複的圖片檔名改成a.jpg')
print('請把要重複的圖片檔名改成b.jpg')

filea='a.jpg'
a1=Image.open(filea)
a2=a1.getdata()
ax,ay=a2.size
aa=list(a2)

fileb='b.jpg'
b1=Image.open(fileb)
b2=b1.getdata()
bx,by=b2.size
bb=list(b2)

x=ax
y=ay
rgba=(0,0,0,0)
q=[]
for i in range(y):
    for j in range(x):
        q.append(rgba)
for i in range(y):
    for j in range(x):
        if((i+j)%2):
            r=aa[j+i*x][0]
            g=aa[j+i*x][1]
            b=aa[j+i*x][2]
            q[j+i*x]=(0,0,0,255-(r+g+b)//3)
        else:
            r=bb[j+i*x][0]
            g=bb[j+i*x][1]
            b=bb[j+i*x][2]
            q[j+i*x]=(255,255,255,(r+g+b)//3)
image_out = Image.new('RGBA',(x,y))
image_out.putdata(q)
image_out.save('1.png')
