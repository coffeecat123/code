import sys
q=''
while True:
    x=input()
    if(x==''):
        break;
    q+=x+'\n'
q=q.replace('&','&amp')
q=q.replace('<','&lt')
q=q.replace('>','&gt')
q=q.replace('\"','&quot')
q=q.replace('\'','&apos')
print(q)
