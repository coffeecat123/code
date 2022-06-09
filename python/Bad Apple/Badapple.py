from toascii import Video
v=Video('yt1s.com - 東方Bad Apple ＰＶ影絵.mp4',
        scale=0.1,verbose=True)
v.convert()
a=0
b=len(v.frames)
print(b)

f=open('4.txt','w')
while a<b:
    c=str(v.frames[a])
    f.write(c+'\n[-]')
    a+=1
f.close()

