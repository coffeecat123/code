from PIL import Image
def qaz(x,y):
    global k
    q0=eval(k.split('=')[0])
    q1=eval(k.split('=')[1])
    return abs(q0-q1)
#-------初始化--------
z=50#每個象限邊方格數
rgb1=(0,255,20)#背景(r,g,b)
rgb2=(255,0,0)#方程式(r,g,b)
rgb3=(0,0,0)#中心點(r,g,b)
c=0#c>=0
q='5*x+y=20'#方程式
#----------------------
q=q.split(',')
xa=z*2
ya=z*2
b=[rgb1]*(xa*ya)
for k in q:
    for i in range(ya):
        for j in range(xa):
            x=j-xa/2
            y=-(i-ya/2)
            if(qaz(x,y)<=c):
                b[round(i*xa+j)]=rgb2
b[int(ya/2)*xa+int((xa)/2)]=rgb3
a=Image.new('RGB',(xa,ya))
a.putdata(b)
a.save('123.png')
'''
a=Image.open('123.png')
a.show()
'''
