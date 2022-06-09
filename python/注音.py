import pyautogui as p
import random as r
import time as t
import threading
p.hotkey('win','up')
p.hotkey('win','right')
p.click(500,500)
p.PAUSE=0
'''
#忘記換輸入法
while True:
    x=input()
    p.click(500,500)
    p.hotkey('ctrl','a')
    p.press('delete')
    for i in x:
        p.press(str(i))
#隨機點字
for i in range(10):
    p.press('`')
    p.press('u')
    p.press('2')
    p.press('8')
    a=r.randint(0,15)
    p.press(hex(a)[2])
    a=r.randint(0,15)
    p.press(hex(a)[2])
    p.press('enter')
'''
