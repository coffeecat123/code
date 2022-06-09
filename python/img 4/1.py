from PIL import Image
print('請把要重複的圖片檔名改成a.jpg')
print('請把要重複的圖片檔名改成b.jpg')
print('請把要重複的圖片檔名改成c.jpg')
print('請把要重複的圖片檔名改成d.jpg')

filea='a.jpg'
a=Image.open(filea)
a2=a.getdata()
ax,ay=a2.size
aa=list(a2)

fileb='b.jpg'
b=Image.open(fileb)
b2=b.getdata()
bx,by=b2.size
bb=list(b2)

filec='c.jpg'
c=Image.open(filec)
c2=c.getdata()
cx,cy=c2.size
cc=list(c2)

filed='d.jpg'
d=Image.open(filed)
d2=d.getdata()
dx,dy=d2.size
dd=list(d2)

x=max(ax,bx,cx,dx)
y=max(ay,by,cy,dy)
rgba=(0,0,0,0)
q=[]
for i in range(y*2):
    for j in range(x*2):
        q.append(rgba)
for i in range(y*2):
    for j in range(x*2):
        if(i%2):
            if(j%2):
                if(j//2<ax and i//2<ay):
                    q[j+i*x*2]=aa[j//2+i//2*ax]
            else:
                if(j//2<bx and i//2<by):
                    q[j+i*x*2]=bb[j//2+i//2*bx]
        else:
            if(j%2):
                if(j//2<cx and i//2<cy):
                    q[j+i*x*2]=cc[j//2+i//2*cx]
            else:
                if(j//2<dx and i//2<dy):
                    q[j+i*x*2]=dd[j//2+i//2*dx]
image_out = Image.new('RGBA',(x*2,y*2))
image_out.putdata(q)
image_out.save('1.png')
