import os
import random as rd
def re(re):
    if(re<=0 or re>=9999
       or re//1000==re//100%10 or re//1000==re//10%10 or re//1000==re%10
      or re//100%10==re//10%10 or re//100%10==re%10 or re//10%10==re%10):
        return 1#重複
    return 0
def d(ad):
    if(ad<1000):
        return '0'+str(ad)
    return ad
def gh(q,w,e,r,a,b):
    global ak
    i=0
    while i<len(ak):
        if (s(q,w,e,r,ak[len(ak)-1-i])[0]!=a or
        s(q,w,e,r,ak[len(ak)-1-i])[1]!=b):
            del ak[len(ak)-1-i]
        else:
            i+=1
def s(a,b,c,d,s):
    e=s//1000
    f=s//100%10
    g=s//10%10
    h=s%10
    q=0
    w=0
    q+=a==e
    q+=b==f
    q+=c==g
    q+=d==h
    w+=a==f
    w+=a==g
    w+=a==h
    w+=b==e
    w+=b==g
    w+=b==h
    w+=c==e
    w+=c==f
    w+=c==h
    w+=d==e
    w+=d==f
    w+=d==g
    return q,w
print('若要讓電腦更精準，請認真回答')
while True:
    print('紀錄答案(方便算):',end='')
    asdlkajb=input()
    a=1
    h=1#次數
    x1=[0]*10#判斷1000
    x2=[0]*10#判斷100
    x3=[0]*10#判斷10
    x4=[0]*10#判斷1
    ak=[]
    for i in range(10000):
        if re(i):
            continue
        ak.append(i)
    k=0
    while a:
        while True:
            print(h,'.',d(ak[k]),sep='',end=' ')
            qa=input('幾A幾B\nA:')
            qb=input('B:')
            if qa.isdigit() and qb.isdigit():
                if(len(qa)==1 and len(qb)==1):
                    if((qa=='0' or qa=='1' or qa=='2' or qa=='3' or qa=='4')
                     and(qb=='0' or qb=='1' or qb=='2' or qb=='3' or qb=='4')):
                        qa=int(qa)
                        qb=int(qb)
                        if qa+qb<=4:
                            break
        if(qa==4):
            a=0
            continue
        q=ak[k]//1000
        w=ak[k]//100%10
        e=ak[k]//10%10
        r=ak[k]%10
        gh(q,w,e,r,qa,qb)
        k=rd.randint(0,len(ak)-1)
        h+=1
    print('猜了',h,'次\n答案是',d(ak[0]))
    gm=input('在玩一次嗎(y/n)')
    while(gm!='y' and gm!='Y' and gm!='n' and gm!='N'):
        gm=input('在玩一次嗎(y/n)')
    if(gm=='n' or gm=='N'):
        break
print('結束')
