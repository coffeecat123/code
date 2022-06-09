def drawPoint(start,end):
    if start==end:
        print(' '*(start-1)+'*')
    else:
        print(' '*(start-1)+'*'+' '*(end-start-1)+'*')
def drawLine(start,end):
    print(' '*(start-1)+'*'*(end-start-1))
def drawCircle():
    drawPoint(3,5)
    drawPoint(2,6)
    drawPoint(3,5)
def drawInsect():
    drawPoint(4,4)
    drawPoint(3,5)
    drawPoint(2,6)
def drawRectangle():
    drawLine(1,9)
    drawPoint(1,7)
    drawPoint(1,7)
    drawPoint(1,7)
    drawLine(1,9)
def drawTriangle():
    drawInsect()
    drawLine(1,9)
def girl():
    drawCircle()
    drawTriangle()
    drawInsect()
def boy():
    drawCircle()
    drawRectangle()
    drawInsect()
def house():
    drawInsect()
    drawRectangle()
