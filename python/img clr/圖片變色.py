from PIL import Image
def atb(a1,a2,a3,b1,b2,b3):
    global i
    '''
    if( c[i][0]==a1
        and c[i][1]==a2
        and c[i][2]==a3):
        c[i]=(b1,b2,b3)
    '''
def qw(a):
    return a*980//1000
file='x.jpg'
im = Image.open(file)
image=im.getdata()
image_out = Image.new(image.mode,image.size)

c = list(im.getdata())
for i in range(len(c)):
    #atb(255,255,255,0,0,0)
    c1=c[i][0]
    c2=c[i][1]
    c3=c[i][2]
    c[i]=(0,0,c3)
#c.reverse()
image_out.putdata(c)
image_out.save('b.png')
c = list(im.getdata())
for i in range(len(c)):
    #atb(255,255,255,0,0,0)
    c1=c[i][0]
    c2=c[i][1]
    c3=c[i][2]
    c[i]=(0,c2,0)
image_out.putdata(c)
image_out.save('g.png')
c = list(im.getdata())
for i in range(len(c)):
    #atb(255,255,255,0,0,0)
    c1=c[i][0]
    c2=c[i][1]
    c3=c[i][2]
    c[i]=(c1,0,0)
image_out.putdata(c)
image_out.save('r.png')
