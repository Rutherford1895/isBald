import numpy as np
import random
import sys
import time
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, qRgb, QTextOption
from PyQt5.QtCore import QRectF, QCoreApplication, Qt, QThread, pyqtSignal

#global conceptNames, conceptsActivity, conceptNumber, proposal, ts, t, currentPosition, loopcounter, head
#concept web
conceptNames = {0:"Bald",1:"not Bald"}
conceptsActivity = {0:0,1:0}
conceptNumber = 2
#proposal to stop
proposal = 0


#temperature
t=100
#current position
currentPosition=[]
#loop counter
loopcounter = 0

#random.seed(123456789)
   
#generate matrix
head = np.ones(shape = (20,20), dtype = np.int32)
#print(self.head)
#set random points to zero
for i in range(320):
    a = random.randint(0,19)
    b = random.randint(0,19)
    head[a][b] = 0
    #print((a,b))
print(head)

class Job(QThread):
    #global conceptNames, conceptsActivity, conceptNumber, proposal, ts, t, currentPosition, loopcounter, head
    signal1 = pyqtSignal(tuple)
    def signal1emit(self,var):
        self.signal1.emit(var)
    
    def __init__(self):
        super(Job, self).__init__()
        #self.signal1.connect(putDot)
        #switch for selecting which kind of task to take
        self.switch={0:self.task0,1:self.task1}
        #state
        self.state=1
        #task sequence
        self.ts = [0]
    
    def run(self):
        #run example_slot_signal loop
        while self.state:
            self.mainloop()
            global loopcounter
            loopcounter += 1
            if loopcounter > 300:
                print("\nToo confusing. Can't solve in 300 runs.")
                break
        
        #post-run output
        print("\nConclusion reached in "+str(loopcounter)+" runs:")
        global conceptNames
        if conceptsActivity[0]>conceptsActivity[1]:
            print(conceptNames[0])
        else:
            print(conceptNames[1])
        print('\nConcepts Activity:\n')
        print(conceptNames[0],conceptsActivity[0])
        print(conceptNames[1],conceptsActivity[1])
    
    #Task: scout
    def task0(self):
        #print("Scouting...")
        randomPosition=(random.randint(0,19),random.randint(0,19))
        global head
        if head[randomPosition[0]][randomPosition[1]] == 1:
            global conceptsActivity
            conceptsActivity[1]+=1
        else:
            conceptsActivity[0]+=1
        self.signal1.emit(randomPosition)
        time.sleep(0.01)
    
    #Task: put forward proposal
    def task1(self):
        #print("Putting forward...")
        global proposal
        proposal += 1
         
    def mainloop(self):
        #print("Main loop starting...")
        self.switch[self.ts[0]]()
        self.ts.pop(0)
        #if difference between concept activities is larger than 10, get temperature -1; smaller than 5, get temperature +1
        global t
        if abs(conceptsActivity[0]-conceptsActivity[1]) > 7 and t >0:
            t -= 1
        elif abs(conceptsActivity[0]-conceptsActivity[1]) < 7 and t <100:
            t += 5
        #if temperature < 30, start to try to put forward a conclusion
        if t <30:
            self.ts.append(random.randint(0,1))
        else:
            self.ts.append(0)
        #proposal weakened with time
        if proposal > 0:
            proposal - 0.5
        #decide to stop when proposal > 15
        if proposal > 15:
            self.state = 0
    
class Window(QWidget):
    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(400,300,200,200)
        self.setWindowTitle("isBald?_multiAgent")
        self.brushes={
            0:QBrush(QColor(0xffffff)),
            1:QBrush(QColor(0x303030))
            }
        self.pos = ()
        self.thread1 = Job()
        self.thread1.signal1.connect(self.update)
        self.thread1.signal1.connect(self.setpos)
        self.thread1.start()
        
    
    def setpos(self,posGot):
        self.pos = posGot
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(0x808080))
        for i in range(20):
            for j in range(20):
                rect = QRectF(j*10,i*10, 10, 10)
                qp.setBrush(self.brushes[head[i][j]])
                qp.drawRect(rect)
        if self.pos != ():
            #print(self.pos)
            qp.setBrush(QColor(0xff4500))
            qp.drawEllipse(2.5+self.pos[1]*10,2.5+self.pos[0]*10,5,5)
        qp.end()
    
app = QApplication(sys.argv)
window1 = Window()
window1.show()
sys.exit(app.exec_())

