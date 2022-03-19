import numpy as np
import time
from threading import Timer
import math


rows = 5
cols = 5
middle =  3-1
#seating = np.zeros([rows, cols])


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

     

    def moveDown(self, seating):
        seating[self.y, self.x] = self.thisnum
        #self.display()
        self.y += 1
        seating[self.y - 1, self.x] = 0

        #time.sleep(1)

    def moveLeft(self, seating):
        seating[self.y, self.x] = self.thisnum
        #self.display()
        self.x -= 1
        seating[self.y, self.x + 1] = 0

        #time.sleep(1)

    def moveRight(self, seating):
        seating[self.y, self.x] = self.thisnum
        #self.display()
        self.x += 1
        seating[self.y, self.x - 1] = 0

        #time.sleep(1)

    def sitDown(self, seating):
        seating[self.y, self.x+1] = self.thisnum
        self.seated=True

    def display(self, seating):
        print(seating)
        print("------------------")


p1 = Passenger(4, 0, 1)
p2 = Passenger(3, 4, 1)
p3 = Passenger(2, 3, 1)
p4 = Passenger(1, 1, 1)


def runProgram():
    seating=np.zeros([rows, cols])
    passengers = [p2,p1,p4,p3]
    ct=0
    numpass=len(passengers)
    while ct<numpass:
            for passenger in passengers:
                if passenger.ent==False  and seating[passenger.y, passenger.x]==0:
                    seating[passenger.y, passenger.x]=passenger.thisnum
                    passenger.ent=True
                elif passenger.ent==True:
                    if passenger.colNum == passenger.x and passenger.rowNum == passenger.y:
                      # passenger.sitDown(seating)
                        passenger.sit=True
                        tmp=0
                        for passenger in passengers:
                             if passenger.sit==True:
                                 tmp+=1
                        if tmp==numpass:
                             ct=numpass
                    elif passenger.rowNum != passenger.y and seating[passenger.y+1, passenger.x]==0:
                        passenger.moveDown(seating)
                        seating[passenger.y-1, passenger.x] = 0
                        seating[passenger.y,passenger.x]=passenger.thisnum
                    elif passenger.colNum < middle and seating[passenger.y, passenger.x-1]==0:
                        if passenger.x != -1:
                             passenger.moveLeft(seating)
                             seating[passenger.y, passenger.x+1]=0
                             seating[passenger.y,passenger.x]=passenger.thisnum

                    elif passenger.colNum != passenger.x and seating[passenger.y, passenger.x+1]==0:
                        passenger.moveRight(seating)
                        seating[passenger.y, passenger.x-1]=0
                        seating[passenger.y,passenger.x]=passenger.thisnum
            if ct!=numpass:
                print(seating)
                print("-------------")
                time.sleep(1)
        




runProgram()
