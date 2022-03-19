import numpy as np
import time
import random
from threading import Timer
import math


rows = int(input("Choose number of rows: "))
cols = int(input("Choose numer of columns: "))
middle =  int(math.ceil(cols/2))-1
Vmin=17*11*7

class Bag:
    def __init__(self):
        self.volume=self.bagvol()

    def bagvol(self):
        l=random.randrange(17,23,1)
        w=random.randrange(11,15,1)
        h=random.randrange(7,10,1)
        return(l*w*h)

class Strategy:
    def __init__(self,type):
        self.type=type
        self.stratarray=self.sarray(type)

    def sarray(self,type):
        sar=[]
        signature=1
        print("array")
        if type==1:  #random
            for r in range(rows):
                for c in range(cols):
                    if c!=middle:
                        sar.append(Passenger(r,c,signature))
                        print("col num:",c)
                        signature=signature+1
            random.shuffle(sar)
        return(sar)

class Passenger:
    def __init__(self, rowNum, colNum, thisnum):
        self.rowNum = rowNum
        self.colNum = colNum
        
        self.x = middle
        self.y = 0
        self.left = False
        self.right = False
        self.ent = False
        self.thisnum = thisnum
        self.sit=False
        self.passinfront=0
        self.age=float(int(np.random.normal(39,19.5,1)))
        self.numbags=self.setbags()
#        print("age",self.age)
        self.atime=self.agetime(self.age)
#        print(self.atime)
        self.Bags=[]
        trackofbags=0
        for k in range(0,self.numbags-1):
            self.Bags.append(Bag())
#            print(self.Bags[k].volume)
            trackofbags=trackofbags+(float(self.Bags[k].volume)/Vmin)
        self.timestore=self.numbags*(trackofbags+self.atime)
#        self.timestore=3
        if self.timestore==0:
            print(self.thisnum,"yeah")
            print("For passenger")
            print(self.thisnum)
            print("bags")
            print(self.numbags)
            print("vol")
            print(trackofbags)
            print("age time")
            print(self.atime)
            print("tot")
    #        print(self.timestore)
           
    def agetime(self,a):
        if a>80:
           a=80
        elif a<3:
           a=3
        if a<25:
           a=(((a/2.5)-10)**2)+3
        else:
           a=(((a/10)-2.5)**2)+3
        return(a)
        
    def setbags(self):
        j=np.random.normal(2,1.5,1)
        if self.age<=10:
           if j<1.5:
              j=0
           else:
              j=1
        elif self.age>=65:
           if j<2:
              j=1
           else:
              j=2
        else: 
           if j<1:
              j=1
           elif j>3:
              j=3
           else:
              j=2
        return(j)

    def moveDown(self, seating):
        seating[self.y, self.x] = self.thisnum
        #self.display()
        self.y += 1
        seating[self.y - 1, self.x] = 0

        #time.sleep(1)

    def moveLeft(self, seating):
       # seating[self.y, self.x] = self.thisnum
        #self.display()
        if self.x>0:
            self.x -= 1
       # seating[self.y, self.x + 1] = 0

        #time.sleep(1)

    def moveRight(self, seating):
       # seating[self.y, self.x] = self.thisnum
        #self.display()
        if self.x<cols-1:
            self.x += 1
       # seating[self.y, self.x - 1] = 0

        #time.sleep(1)

    def sitDown(self, seating):
       # seating[self.y, self.x+1] = self.thisnum
        self.seated=True

    def display(self, seating):
        print(seating)
        print("------------------")


p1 = Passenger(4, 0, 2)
p2 = Passenger(3, 4, 3)
p3 = Passenger(2, 3, 4)
p4 = Passenger(1, 1, 5)


def runProgram():
    seating=np.zeros([rows, cols])
    passengers = Strategy(1).stratarray
    ct=0
    t=0
    numpass=len(passengers)
    while ct<numpass:
            for passenger in passengers:
                if passenger.ent==False and seating[passenger.y, passenger.x]==0:
                    seating[passenger.y, passenger.x]=passenger.thisnum
                    passenger.ent=True
                elif passenger.ent==True:
                    if passenger.rowNum != passenger.y and seating[passenger.y+1, passenger.x]==0:
                        passenger.moveDown(seating)
                        seating[passenger.y-1, passenger.x] = 0
                        seating[passenger.y,passenger.x]=passenger.thisnum
                    elif passenger.rowNum==passenger.y and passenger.timestore>0:
                        passenger.timestore=passenger.timestore-1
                    elif passenger.timestore<=0 and passenger.sit==False and passenger.rowNum==passenger.y:
                        test=0
                        if passenger.colNum < middle and passenger.x>-1:
                             if seating[passenger.y,passenger.x]==passenger.thisnum:
                                 seating[passenger.y, passenger.x]=0
                                 test+=1
                             if seating[passenger.y, passenger.x-1]==0:
                                 test+=1
                                 seating[passenger.y,passenger.x-1]=passenger.thisnum
                             if test!=2 and passenger.passinfront!=2:
                                 passenger.passinfront+=1
                             if test==2 or passenger.passinfront==2:
                                 passenger.moveLeft(seating)
                                 passenger.passinfront=0

                        elif passenger.colNum != passenger.x and passenger.x<cols:
                             if seating[passenger.y,passenger.x]==passenger.thisnum:
                                 test+=1
                                 seating[passenger.y, passenger.x]=0
                             if seating[passenger.y, passenger.x+1]==0:
                                 test+=1
                                 seating[passenger.y,passenger.x+1]=passenger.thisnum
                             if test!=2 and passenger.passinfront!=2:
                                 passenger.passinfront+=1
                             if test==2 or passenger.passinfront==2:
                                 passenger.moveRight(seating)
                                 passenger.passinfront=0
                    if passenger.colNum == passenger.x and passenger.rowNum == passenger.y:
                      # passenger.sitDown(seating)
                        seating[passenger.y, passenger.x] = passenger.thisnum
                        passenger.sit=True
                        tmp=0
                        for passenger in passengers:
                             if passenger.sit==True:
                                 tmp+=1
                       # print(tmp)
                        if tmp==numpass:
                             ct=numpass
           # if ct!=numpass:
            t+=1
            print(seating)
            print("-------------")
           # time.sleep(1)
    print(float(t)/60)    




runProgram()
