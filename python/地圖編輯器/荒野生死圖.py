import turtle as tl
import tkinter as tk
import tkinter.messagebox as tm
import tkinter.colorchooser as cc
import tkinter.font as tkFont
import os
from PIL import Image

def qtw(x,y):
    global za,rgb1,sx,sy,vv,vv2,vv3,ma
    ptx,pty=x,y
    stackx,stacky=[],[]
    stackx.append(ptx)
    stacky.append(pty)
    while(stackx):
        x=ptx=stackx.pop()
        y=pty=stacky.pop()
        if(vv2):
            while(qcr[int(x+y*sx)]==vv3):
                df(x*za-za/2*(sx-1),y*za-za/2*(sy-1),1)
                x+=1
                if(x>=sx or x<0):
                    break
        else:
            while(qa[int(x+y*sx)]==0):
                df(x*za-za/2*(sx-1),y*za-za/2*(sy-1),1)
                x+=1
                if(x>=sx or x<0):
                    break
        xr=x-1
        x=ptx-1
        if(vv2):
            if(x<sx and x>=0):
                while(qcr[int(x+y*sx)]==vv3):
                    df(x*za-za/2*(sx-1),y*za-za/2*(sy-1),1)
                    x-=1
                    if(x>=sx or x<0):
                        break
        else:
            if(x<sx and x>=0):
                while(qa[int(x+y*sx)]==0):
                    df(x*za-za/2*(sx-1),y*za-za/2*(sy-1),1)
                    x-=1
                    if(x>=sx or x<0):
                        break
        xl=x+1
        
        #處理上一條掃描線
        if(pty-1>=0):
            x=xl
            y=pty-1
            while(x<=xr):
                sf=0
                if(vv2):
                    while(qcr[int(x+y*sx)]==vv3):
                        sf=1
                        x+=1
                        if(x>=sx or x<0):
                            break
                else:
                    while(qa[int(x+y*sx)]==0):
                        sf=1
                        x+=1
                        if(x>=sx or x<0):
                            break
                if(sf):
                    stackx.append(x-1)
                    stacky.append(y)
                if(vv2):
                    if(x<sx and x>=0):
                        while(qcr[int(x+y*sx)]!=vv3 and x<=xr):
                            x+=1
                            if(x>=sx or x<0):
                                break
                else:
                    if(x<sx and x>=0):
                        while(qa[int(x+y*sx)]!=0 and x<=xr):
                            x+=1
                            if(x>=sx or x<0):
                                break
        #處理下一條掃描線，程式碼與處理上一條掃描線類似
        if(pty+1<sy):
            x=xl
            y=pty+1
            while(x<=xr):
                sf=0
                if(vv2):
                    while(qcr[int(x+y*sx)]==vv3):
                        sf=1
                        x+=1
                        if(x>=sx or x<0):
                            break
                else:
                    while(qa[int(x+y*sx)]==0):
                        sf=1
                        x+=1
                        if(x>=sx or x<0):
                            break
                if(sf):
                    stackx.append(x-1)
                    stacky.append(y)
                if(vv2):
                    if(x<sx and x>=0):
                        while(qcr[int(x+y*sx)]!=vv3 and x<=xr):
                            x+=1
                            if(x>=sx or x<0):
                                break
                else:
                    if(x<sx and x>=0):
                        while(qa[int(x+y*sx)]!=0 and x<=xr):
                            x+=1
                            if(x>=sx or x<0):
                                break
            
def af(x,y):
    global qa,qcr,sa,za,sx,sy,vv,vv2,vv3,rgb1,ma
    tl.pu()
    if(abs(x)<=za*(sx/2) and abs(y)<=za*(sy/2)):
        x1=(x+za*(sx/2))//za*za-za*(sx/2)+za/2
        y1=(y+za*(sy/2))//za*za-za*(sy/2)+za/2
        tl.pu()
        vv2=qa[int((x1+za*(sx/2))//za+(y1+za*(sy/2))//za*sx)]
        if(vv2):
            vv3=qcr[int((x1+za*(sx/2))//za+(y1+za*(sy/2))//za*sx)]
        if(vv):
            tl.goto(x1,y1)
            if(sa):
                if(qcr[int((x1+za*(sx/2))//za+(y1+za*(sy/2))//za*sx)]==rgb1):
                    return 0
            else:
                if(qa[int((x1+za*(sx/2))//za+(y1+za*(sy/2))//za*sx)]==0):
                    return 0
            ma=0
            qtw((x1+za*(sx/2))//za,(y1+za*(sy/2))//za)
            tl.goto(x1,y1)
        else:
            df(x1,y1,1)
def line():
    global za,rgb2,rgb3,rgb4,pa,ba,sx,sy
    a=tl.heading()
    tl.color(rgb3)
    tl.seth(0)
    for i in range(sy+1):
        tl.pu()
        tl.goto(-za*(sx/2),-za*(sy/2)+i*za)
        tl.pd()
        tl.fd(za*sx)
    tl.seth(90)
    for i in range(sx+1):
        tl.pu()
        tl.goto(-za*(sx/2)+i*za,-za*(sy/2))
        tl.pd()
        tl.fd(za*sy)
    tl.pu()
    tl.seth(a)
    tl.color(rgb4)
def df(x,y,a):
    global sa,za,ma,rgb1,rgb2,rgb3,rgb4,qcr,sx,sy
    if(abs(x)>za*(sx/2) and abs(y)>za*(sy/2)):
        return 0
    if(a==1):
        if(ma==1):
            df(x,-y,0)
        if(ma==2):
            df(-x,y,0)
        if(ma==3):
            df(-x,-y,0)
        if(ma==4):
            df(x,-y,0)
            df(-x,y,0)
            df(-x,-y,0)
        if(ma==5):
            df(-y,x,0)
            df(y,-x,0)
            df(-x,-y,0)
    if(sa==1):
        tl.color(rgb1)
        qa[int((x+za*(sx/2))//za+(y+za*(sy/2))//za*sx)]=1
        qcr[int((x+za*(sx/2))//za+(y+za*(sy/2))//za*sx)]=rgb1
    else:
        tl.color(rgb2)
        qa[int((x+za*(sx/2))//za+(y+za*(sy/2))//za*sx)]=0
        qcr[int((x+za*(sx/2))//za+(y+za*(sy/2))//za*sx)]=rgb2
    tl.pu()
    tl.goto(x,y)
    tl.fd(za/2)
    tl.lt(90)
    tl.pencolor(rgb3)
    tl.begin_fill()
    tl.pd()
    tl.fd(za/2)
    tl.lt(90)
    tl.fd(za)
    tl.lt(90)
    tl.fd(za)
    tl.lt(90)
    tl.fd(za)
    tl.lt(90)
    tl.fd(za/2)
    tl.end_fill()
    tl.pu()
    tl.lt(90)
    tl.fd(za/2)
    tl.lt(180)
    tl.color(rgb4)
#-------鍵盤----------
def b():
    global ba,za,sa,sx,sy,sz,ba1
    if(100/ba*((sx*sy)**0.5/2+1)*2>4*za):
        ba*=2
    else:
        ba=za
    tl.turtlesize(ba/16,ba/16)
    for i in range(ba1):
        if(tl.turtlesize()[0]<ba/4):
            tl.turtlesize(tl.turtlesize()[0]*2,tl.turtlesize()[1]*2)
        else:
            tl.turtlesize(ba/16,ba/16)
    a=100/ba*(sz/2+1)
    tl.setworldcoordinates(-a,-a,a,a)
    tl.screensize(ba*64,ba*64)
    sa=1
def c():
    global sx,sy,la
    la=0
    sx1=sy1=0
    if(sx%2==0):
        sx1=za/2
    if(sy%2==0):
        sy1=za/2
    tl.goto(sx1,sy1)
def e():
    global sa
    if(sa==0):
        sa=1
    else:
        sa=0
def f():
    global za,qa,qcr,rgb2,sx,sy
    tx,ty=tl.xcor(),tl.ycor()
    qa=[0]*(sx*sy)
    qcr=[rgb2]*(sx*sy)
    tl.clear()
    line()
    tl.goto(tx,ty)
def g():
    global ba,ba1
    if(tl.turtlesize()[0]<ba/4):
        tl.turtlesize(tl.turtlesize()[0]*2,tl.turtlesize()[1]*2)
        ba1+=1
    else:
        tl.turtlesize(ba/16,ba/16)
        ba1=0
def h():
    global ma
    if(ma==1):
        ma=0
    else:
        ma=1
def i():
    global ma
    if(ma==2):
        ma=0
    else:
        ma=2
def j():
    global ma
    if(ma==3):
        ma=0
    else:
        ma=3
def k():
    global ma
    if(ma==4):
        ma=0
    else:
        ma=4
def l():
    global ma,sx,sy
    if(sx==sy):
        if(ma==5):
            ma=0
        else:
            ma=5
def m():
    df(tl.xcor(),tl.ycor(),1)
def n():
    global ka
    if(ka==0):
        tl.showturtle()
        ka=1
    else:
        tl.hideturtle()
        ka=0
def o():
    global rgb1
    a=rgb1
    try:
        rgb1=cc.askcolor()[0]
        tl.fillcolor(rgb1)
    except:
        rgb1=a
    tl.listen()
def p():
    global rgb2,rgb3,rgb4,qa,qcr,za,sx,sy
    tx,ty=tl.xcor(),tl.ycor()
    a=rgb2
    try:
        rgb2=cc.askcolor()[0]
        #tm.showinfo(title='python',message='pls wait')
        for i in range(sy):
            for j in range(sx):
                if(qcr[i*sx+j]==a and qa[i*sx+j]==0):
                    qcr[i*sx+j]=rgb2
                    tl.pu()
                    tl.goto(j*za-sx*za/2,i*za-sy*za/2)
                    tl.pencolor(rgb3)
                    tl.fillcolor(rgb2)
                    tl.begin_fill()
                    tl.pd()
                    tl.fd(za)
                    tl.lt(90)
                    tl.fd(za)
                    tl.lt(90)
                    tl.fd(za)
                    tl.lt(90)
                    tl.fd(za)
                    tl.lt(90)
                    tl.fd(za)
                    tl.end_fill()
        tl.pu()
        tl.goto(tx,ty)
        tl.color(rgb4)
        tl.bgcolor(rgb2)
        #tm.showinfo(title='python',message='Ok!')
    except:
        rgb2=a
        tl.bgcolor(a)
    tl.listen()
def q():
    global rgb3
    tx,ty=tl.xcor(),tl.ycor()
    a=rgb3
    try:
        rgb3=cc.askcolor()[0]
        line()
    except:
        rgb3=a
    tl.goto(tx,ty)
    tl.listen()
def r():
    global rgb4
    a=rgb4
    try:
        rgb4=cc.askcolor()[0]
        tl.color(rgb4)
    except:
        rgb4=a
    tl.listen()
def t():
    global ka,va
    if(tl.bgpic()!='nopic'):
        tl.bgpic('nopic')
    else:
        tl.bgpic('bs/'+str(va)+'.png')
def u():
    global va
    va+=1
    try:
        tl.bgpic('bs/'+str(va)+'.png')
    except:
        va=1
        tl.bgpic('bs/'+str(va)+'.png')
def v():
    global vv
    if(vv==1):
        vv=0
    else:
        vv=1
def z():
    global qa,qcr
    print(qa)
    print(qcr)
def sp():
    global la
    if(la==1):
        la=0
    else:
        la=1
#-------file---------
def sdf():
    global sa,za,rgb2,rgb4,qa,qcr,pa,sx,sy,ba
    tl.clear()
    tl.seth(0)
    sa=1
    for i in range(sy):
        tl.pu()
        tl.goto(-za*(sx/2)+za/2,-za*(sy/2)+i*za)
        for j in range(sx):
            rgb1=qcr[i*sx+j]
            if rgb1!=rgb2:
                qa[i*sx+j]=1
            tl.pencolor(rgb3)
            tl.fillcolor(rgb1)
            tl.begin_fill()
            tl.pd()
            tl.fd(za/2)
            tl.lt(90)
            tl.fd(za)
            tl.lt(90)
            tl.fd(za)
            tl.lt(90)
            tl.fd(za)
            tl.lt(90)
            tl.fd(za/2)
            tl.end_fill()
            if(j<sx-1):
                tl.fd(za)
    tl.pu()
    sx1=sy1=0
    if(sx%2==0):
        sx1=za/2
    if(sy%2==0):
        sy1=za/2
    tl.goto(sx1,sy1)
    tl.seth(0)
    pa='rt'
    tl.color(rgb4)
    tl.screensize(ba*64,ba*64)
    a=100/ba*(sz/2+1)
    tl.setworldcoordinates(-a,-a,a,a)
def read():#讀檔y
    global qa,qcr,za,rgb1,rgb2,rgb3,rgb4,pa,ka,ma,va,ba,sx,sy,sz
    x=input("請輸入要匯入的檔名：")
    if(len(x)>=4):
        if(a[-4:]!='.txt'):
            x+='.txt'
    else:
        x+='.txt'
    try:
        with open('map.txt/'+x,'r') as f:
            print("Wait!")
            a=f.read()
            qa=eval(a.split("=")[0])
            qcr=eval(a.split("=")[1])
            za=int(a.split("=")[2])
            rgb1=eval(a.split("=")[3])
            rgb3=eval(a.split("=")[5])
            rgb4=eval(a.split("=")[6])
            pa=str(a.split("=")[7])
            ka=int(a.split("=")[8])
            ma=int(a.split("=")[9])
            va=int(a.split("=")[10])
            sx=int(a.split("=")[11])
            sy=int(a.split("=")[12])
            if(sx>sy):
                sz=sx
            else:
                sz=sy
            sdf()
            rgb2=eval(a.split("=")[4])
            ba=za
            tl.bgcolor(rgb2)
            line()
            tl.color(rgb4)
            print("Ok!")
    except:
        print('沒找到指定檔案(要放在"map.txt"資料夾裡)')
def save():#x存檔
    global qa,qcr,za,rgb1,rgb2,rgb3,rgb4,pa,ka,ma,va,sx,sy,sz
    if(not os.path.exists("map.txt")):
        os.mkdir("map.txt")
    if(not os.path.exists("map.png")):
        os.mkdir("map.png")
    k=1
    while(os.path.isfile('map.txt/'+str(k)+'.txt') or
          os.path.isfile('map.png/'+str(k)+'.png')):
        k+=1
    b=[0]*(sx*sy)
    for i in range(sy):
        for j in range(sx):
            b[i*sx+j]=qcr[(sy-1-i)*sx+j]
    a=Image.new('RGB',(sx,sy))
    a.putdata(b)
    a.save('map.png\\'+str(k)+'.png')
    with open('map.txt/'+str(k)+'.txt','w') as f:
        f.write(str(qa)
                +"="+str(qcr)
                +"="+str(za)
                +"="+str(rgb1)
                +"="+str(rgb2)
                +"="+str(rgb3)
                +"="+str(rgb4)
                +"="+str(pa)
                +"="+str(ka)
                +"="+str(ma)
                +"="+str(va)
                +"="+str(sx)
                +"="+str(sy))
        tm.showinfo(title='python',message=f'已儲存在"map.txt"資料夾，名為:{k}(.txt)')
        print(f'已儲存在"map.txt"資料夾，名為:{k}(.txt)')
#-----上下左右------
def rt():
    global pa,sx
    if(pa=='rt'):
        tl.fd(za)
    else:
        tl.seth(0)
        pa='rt'
    if(abs(tl.xcor())>(sx/2)*za):
        tl.undo()
def lt():
    global pa,sx
    if(pa=='lt'):
        tl.fd(za)
    else:
        tl.seth(180)
        pa='lt'
    if(abs(tl.xcor())>(sx/2)*za):
        tl.undo()
def up():
    global pa,sy
    if(pa=='up'):
        tl.fd(za)
    else:
        tl.seth(90)
        pa='up'
    if(abs(tl.ycor())>(sy/2)*za):
        tl.undo()
def dw():
    global pa,sy
    if(pa=='dw'):
        tl.fd(za)
    else:
        tl.seth(-90)
        pa='dw'
    if(abs(tl.ycor())>(sy/2)*za):
        tl.undo()
    
'''
b:放大
c:回原點
e:橡皮擦
f:清空
g:放大turtle
h:上下對稱
i:左右對稱
j:中心對稱
k:上下+左右對稱
l:旋轉對稱
m:單格填滿
n:turtle顯示/隱藏
o:填滿的顏色
p:背景色(要等一下)
q:格線顏色
r:turtle顏色
t:背景圖片 顯示/隱藏
u:下一張背景
v:倒汁
x:存檔
y:讀檔
z:往回(目前無法使用)
space:連續填滿
上下左右(wsad):
'''
#-----初始化-------
while(1):
    try:
        sx=int(input('請輸入畫布行數(1~300):'))
        if(sx>0 and sx<=300):
            break
        else:
            print('超出範圍')
    except:
        print('必須是正整數')
while(1):
    try:
        sy=int(input('請輸入畫布列數(1~300):'))
        if(sy>0 and sy<=300):
            break
        else:
            print('超出範圍')
    except:
        print('必須是正整數')
if(sx>sy):
    sz=sx
else:
    sz=sy
za=10#方格邊長(不用改
ba=za#放大
ba1=0
size=660#視窗size
rgb1=(0,0,0)#填滿的顏色
rgb2=(255,255,255)#背景色
rgb3=(0,0,0)#格線顏色
rgb4=(255,0,0)#turtle顏色
qa=[0]*(sx*sy)
qcr=[rgb2]*(sx*sy)
pa='rt'#方向
la=0#畫
ka=1#turtle顯示?
ma=0#對稱方式
sa=1#橡皮擦
va=1#背景圖片
vv=0#倒汁
vv2=0#倒汁2
vv3=(255,255,255)#倒汁3


w2=tk.Tk()
font1=tkFont.Font(family="Arial", size=15, weight="bold", slant="italic")
w2.title('use')
w2.geometry('+0+0')
w2.title('use')
f1=tk.Label(w2,text='',font=font1)
f1.pack()
x1,y1=za/2,za/2
tl.setup(size,size)
a=100/ba*(sz/2+1)
tl.setworldcoordinates(-a,-a,a,a)
tl.st()
#tl.speed(0)
#tl.delay(0)
tl.tracer(False)
tl.colormode(255)
tl.bgcolor(rgb2)
line()
tl.pu()
tl.seth(0)
sx1=sy1=0
if(sx%2==0):
    sx1=za/2
if(sy%2==0):
    sy1=za/2
tl.goto(sx1,sy1)
tl.color(rgb4)
'''
..........3599
3031.......59
 0 1 2.....29
'''
tl.onscreenclick(af)
tl.ondrag(af)
tl.onkeypress(b,'b')
tl.onkeypress(c,'c')
tl.onkeypress(e,'e')
tl.onkeypress(f,'f')
tl.onkeypress(g,'g')
tl.onkeypress(h,'h')
tl.onkeypress(i,'i')
tl.onkeypress(j,'j')
tl.onkeypress(k,'k')
tl.onkeypress(l,'l')
tl.onkeypress(m,'m')
tl.onkeypress(n,'n')
tl.onkeypress(o,'o')
tl.onkeypress(p,'p')
tl.onkeypress(q,'q')
tl.onkeypress(r,'r')
tl.onkeypress(t,'t')
tl.onkeypress(u,'u')
tl.onkeypress(v,'v')
tl.onkeypress(save,'x')
tl.onkeypress(read,'y')
tl.onkeypress(z,'z')
tl.onkeypress(sp,'space')
tl.onkeypress(rt,'Right')
tl.onkeypress(lt,'Left')
tl.onkeypress(up,'Up')
tl.onkeypress(dw,'Down')
tl.onkeypress(rt,'d')
tl.onkeypress(lt,'a')
tl.onkeypress(up,'w')
tl.onkeypress(dw,'s')
tl.listen()
while True:
    try:
        f1['text'] =f'\
b:放大 {str(int(ba/za))}x\n\
c:回原點\n\
e:橡皮擦{sa^1}\n\
f:清空\n\
g:放大turtle\n\
h:上下對稱(1)\n\
i:左右對稱(2)\n\
j:中心對稱(3)\n\
k:上下+左右對稱(4)\n\
l:旋轉對稱(5)\n\
m:單格填滿\n\
n:turtle顯示/隱藏\n\
o:填滿的顏色{rgb1}\n\
p:背景色(要等一下){rgb2}\n\
q:格線顏色{rgb3}\n\
r:turtle顏色{rgb4}\n\
t:背景圖片 顯示/隱藏\n\
u:下一張背景\n\
v:倒汁{vv}\n\
x:存檔\n\
y:讀檔\n\
z:往回(目前無法使用)\n\
space:連續填滿{la}\n\
上下左右(wsad): {pa}\n\
對稱方式:{str(ma)}'
        
        if(la==1):
            df(tl.xcor(),tl.ycor(),1)
        tl.update()
        w2.update()
    except:
        quit()
