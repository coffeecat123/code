import pyautogui as p
import time as t
p.hotkey('win','up')
p.click(1264,12)
p.click(400,400)
t.sleep(1)
p.PAUSE=0
for i in range(5):
    t.sleep(1)
    a=p.pixel(400,400)
    while(a[0]==230):
        a=p.pixel(400,400)
    p.click(400,400)
    a=p.pixel(400,400)
    while(a[0]!=230):
        a=p.pixel(400,400)
