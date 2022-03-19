import numpy as np
import time
import random
from threading import *
import math
from PyView import *

capacity = int(input("Plane capacity: "))
rows = int(input("Plane rows: "))
cols =  = int(input("Plane columns: "))
#capacity = 132
#rows = 23
#cols = 7
middle = int(math.ceil(cols / 2)) - 1
#seating = np.zeros([rows, cols])
Vmin = 17 * 11 * 7
Vmid = 19 * 13 * 8
processes = []
import pandas as pd


class Bag:
  def __init__(self):
    self.volume = self.bagvol()

  def bagvol(self):
    l = random.randrange(17, 23, 1)
    w = random.randrange(11, 15, 1)
    h = random.randrange(7, 10, 1)
    return(l * w * h)
  
  def volconst(self):
    sk=self.volume/Vmid
    return(sk)

  def volconst(self):
    sk=self.volume/Vmid
    return(sk)

class Passenger:

  def __init__(self, rowNum, colNum, thisnum, passNum):
    self.passNum = passNum

    self.rowNum = rowNum
    self.colNum = colNum

    self.seated = False

    self.x = middle
    self.y = 0
    self.left = False
    self.right = False
    self.ent = False
    self.thisnum = thisnum
    self.sit = False
    self.age = float(int(np.random.normal(39, 19.5, 1)))
    self.numbags = self.setbags()
    self.atime = self.agetime(self.age)
    self.Bags = []
    trackofbags = 0

    self.timestore = 0

    for k in range(0, self.numbags):
      self.Bags.append(Bag())
      self.timestore = self.timestore + (float(self.Bags[k].volconst())*self.atime)

    self.timestore = int(self.timestore)

    self.passInFront = 0
    self.speed = 1

    self.mem = '_'

  def agetime(self, a):
    if a>80:
      a=80
    elif a<3:
      a=3
    if a < 25:
      a = (((a / 4) - 6.25)**2) + 5
    else:
      a = (((a / 11.5) - (25/11.5))**2) + 5
    return(a)

  def setbags(self):
    j = random.randrange(100)
    if self.age <= 10:
      if j < 40:
        j = 0
      else:
        j = 1
    elif self.age > 65:
      if j < 40:
        j = 1
      else:
        j = 2
    else:
      if j < 10:
        j = 1
      elif j > 89:
        j = 3
      else:
        j = 2
    return(j)

  def moveDown(self, seating):
    self.y += 1
    seating[self.y][self.x] = self.thisnum
    seating[self.y - 1][self.x] = '_'

  def moveLeft(self, seating):
    if seating[self.y][self.x-1] == 's' and self.passInFront != 1:
      self.passInFront = 1

    elif seating[self.y][self.x-1] == '_' or  self.passInFront != 0:
      tmp = seating[self.y][self.x-1]
      if self.passInFront != 0:
        self.passInFront -= 1
      self.x -= 1
      seating[self.y][self.x] = self.thisnum
      seating[self.y][self.x+1] = self.mem
      self.mem = tmp

  def moveRight(self, seating):
    if seating[self.y][self.x+1] == 's' and self.passInFront != 1:
      self.passInFront = 1

    elif seating[self.y][self.x+1] == '_' or  self.passInFront != 0:
      tmp = seating[self.y][self.x+1]
      if self.passInFront != 0:
        self.passInFront -= 1
      self.x += 1
      seating[self.y][self.x] = self.thisnum
      seating[self.y][self.x-1] = self.mem
      self.mem = tmp

  def sitDown(self, seating):
    self.seated = True
    self.thisNum = 's'
    seating[self.y][self.x] = self.thisNum

  def display(self, seating):
    print(seating)
    print("------------------")

  def update(self, seating):
    # Enter plane from top middle one at a time:
    if self.ent == False and seating[0][middle] == '_':
      self.ent = True
      seating[0][middle] == self.thisnum
      self.y -= 1
      self.moveDown(seating)

    # For each standing passenger in plane
    elif self.ent == True and self.seated == False:

      # At correct seat -> sit down
      if self.y == self.rowNum and self.x == self.colNum:
        self.sitDown(seating)

      # At correct row -> move to correct seat
      elif self.y == self.rowNum:

        # Stow bags
        if self.timestore > 0 and (self.y >= rows -1 or seating[self.y+1][self.x] == '_'):
          self.timestore -= 1
        # Move left
        elif self.timestore == 0 and self.x > self.colNum and isEmpty(seating, self.x - 1, self.y):
          self.moveLeft(seating)
        # Move right
        elif self.timestore == 0 and self.x < self.colNum and isEmpty(seating, self.x + 1, self.y):
          self.moveRight(seating)

      # Incorrect row -> move down
      elif self.y < self.rowNum and isEmpty(seating, self.x, self.y + 1):
        self.moveDown(seating)


class gPassenger(Passenger):
  def __init__(self, rowNum, colNum, thisnum, sprite, passNum):
    super().__init__(rowNum, colNum, thisnum, passNum)
    self.sprite = sprite
    processes.append([self.passNum, "down"])

  def moveDown(self, seating, processes):
    super().moveDown(seating)
    processes.append([self.passNum, "down"])
    return processes

  def moveLeft(self, seating, processes):
    super().moveLeft(seating)

    if self.passInFront != 0 and self.speed == 1:
      processes.append([self.passNum, "half"])
      self.speed = 0.5
    elif self.passInFront == 0 and self.speed == 0.5:
      processes.append([self.passNum, "double"])
      self.speed = 1

    processes.append([self.passNum, "left"])
    return processes

  def moveRight(self, seating, processes):
    super().moveRight(seating)

    if self.passInFront != 0 and self.speed == 1:
      processes.append([self.passNum, "half"])
      self.speed = 0.5
    elif self.passInFront == 0 and self.speed == 0.5:
      processes.append([self.passNum, "double"])
      self.speed = 1

    processes.append([self.passNum, "right"])
    return processes

  def sitDown(self, seating, processes):
    super().sitDown(seating)
    processes.append([self.passNum, "sit"])
    return processes

  def update(self, seating, processes):
    # Enter plane from top middle one at a time:
    if self.ent == False and seating[0][middle] == '_':
      self.ent = True
      seating[0][middle] == self.thisnum
      self.y -= 1
      processes = self.moveDown(seating, processes)

    # For each standing passenger in plane
    elif self.ent == True and self.seated == False:

      # At correct seat -> sit down
      if self.y == self.rowNum and self.x == self.colNum:
        processes = self.sitDown(seating, processes)

      # At correct row -> move to correct seat
      elif self.y == self.rowNum:

        # Stow bags
        if self.timestore > 0:
          seating[self.y][self.x]='X'
          if isEmpty(seating,self.x,self.y+1):
            self.timestore -= 1
            if self.x > self.colNum:
              processes.append([self.passNum, "stowL"])
            else:
              processes.append([self.passNum, "stowR"])
          else:
              processes.append([self.passNum, "nothingR"])
        # Move left
        elif self.timestore == 0 and self.x > self.colNum and isEmpty(seating, self.x - 1, self.y):
          processes = self.moveLeft(seating, processes)
        # Move right
        elif self.timestore == 0 and self.x < self.colNum and isEmpty(seating, self.x + 1, self.y):
          processes = self.moveRight(seating, processes)

      # Incorrect row -> move down
      elif self.y < self.rowNum and isEmpty(seating, self.x, self.y + 1):
        processes = self.moveDown(seating, processes)

    return processes


def isEmpty(arr, x, y):
  if y>rows-1:
    return True
  if arr[y][x] == 's' or arr[y][x] == '_':
    return True
  else:
    return False


def allSeated(arr):
  for p in arr:
    if p.seated == False:
      return False
  return True


def initSeating(rows, cols):
  seating = []
  for i in range(0, rows):
    seating.append([])
    for j in range(0, cols):
      seating[i].append('_')
  return seating

def randomBoarding(num, plane, views):

  # creates list of (num) passengers
  # (plane) indicates the number of rows and columns
  # for 132 seats, plane = [23, 7]
  # views corresponds to v.passengers

  seating = []

  for i in range(0, plane[0]):
    for j in range(0, plane[1]):
      if((i == 0 or i == plane[0] - 1) and (j == 0 or j == 1 or j == plane[1] - 1)):
        pass
      elif j != middle:
        seating.append([i, j])

  passengers = []

  for i in range(0, num):
    index = random.randint(0, len(seating) - 1)
    coord = seating[index]

    if views == []:
      # information pertaining to view not needed if [] is passed in for views
      passengers.append(Passenger(coord[0], coord[1], 'X', i))
    else:
      passengers.append(gPassenger(coord[0], coord[1], 'X', views[i], i))
    seating.remove(coord)

  return passengers


def steffensOptimalBoarding(num, plane, views):

  passengers = []

  for j in range(0, 3):
    # Loop works outside in
    for i in range(plane[0] - 1, -1, -2):

      # Every other seat starting in back right

      if j == 0 and (i == 0 or i == plane[0] - 1):
        # Skips places where there are no seats
        pass
      else:
        if views == []:
          # information pertaining to view not needed if [] is passed in for views
          passengers.append(Passenger(i, 6 - j, 'X', len(passengers)))
        else:
          passengers.append(gPassenger(i, 6 - j, 'X', views[len(passengers)], len(passengers)))

    for i in range(plane[0] - 1, -1, -2):

      # Every other seat starting in back left

      if (j == 0 or j == 1) and (i == 0 or i == plane[0] - 1):
        # Skips places where there are no seats
        pass
      else:
        if views == []:
          # information pertaining to view not needed if [] is passed in for views
          passengers.append(Passenger(i, j, 'X', len(passengers)))
        else:
          passengers.append(gPassenger(i, j, 'X', views[len(passengers)], len(passengers)))

    for i in range(plane[0] - 2, -1, -2):

      # Every other seat starting one up from back right

      if views == []:
        # information pertaining to view not needed if [] is passed in for views
        passengers.append(Passenger(i, 6 - j, 'X', len(passengers)))
      else:
        passengers.append(gPassenger(i, 6 - j, 'X', views[len(passengers)], len(passengers)))

    for i in range(plane[0] - 2, -1, -2):

      # Every other seat starting one up from back left

      if views == []:
        # information pertaining to view not needed if [] is passed in for views
        passengers.append(Passenger(i, j, 'X', len(passengers)))
      else:
        passengers.append(gPassenger(i, j, 'X', views[len(passengers)], len(passengers)))

  return passengers


def outsideInBoarding(num, plane, views):
  passengers = []

  g = [[], [], []]

  for i in range(0, 3):
    # Creates three groups of seats: rows 0 and 6, rows 1 and 5, and rows 2 and 4
    for j in range(0, plane[0]):

      if (i == 0 or i == 1) and (j == 0 or j == plane[0] - 1):
        # Does not list places with no seats
        pass
      else:
        g[i].append([i, j])

      if i == 0 and (j == 0 or j == plane[0] - 1):
        # Does not list places with no seats
        pass
      else:
        g[i].append([plane[1] - 1 - i, j])

  p = 0

  for i in range(0, 3):
    # Randomly assigns passengers to seats in each group, starting from outside group, working in
    for j in range(0, len(g[i])):
      index = random.randint(0, len(g[i]) - 1)
      coord = g[i][index]

      if views == []:
        # information pertaining to view not needed if [] is passed in for views
        passengers.append(Passenger(coord[1], coord[0], 'X', p))
      else:
        passengers.append(gPassenger(coord[1], coord[0], 'X', views[p], p))

      g[i].remove(coord)
      p += 1

  return passengers

def optimalStrategy(num, plane, views):

    passengers = []

    # Group 1: Board all of the even rows on the left side
    # Group 2: Board all of the even rows on the right side
    # Group 3: Board all of the odd rows on the left side
    # Group 4: Board all of the odd rows on the right side

    group1 = []
    group2 = []
    group3 = []
    group4 = []

    for j in range(0,3):
      # Board all of the even rows on the left side
      for i in range(plane[0] -1, -1, -2):

        if (j == 0 or j == 1) and (i == 0 or i == plane[0] - 1):
            # Skips places where there are no seats
            pass
        else:
          group1.append([i,j])
          random.shuffle(group1)

    for j in range(0,3):
        # Board all of the even rows on the right side
        for i in range(plane[0] - 1, -1, -2):

          if j == 0 and (i == 0 or i == plane[0] - 1):

            pass
          else:
            group2.append([i,6-j])
            random.shuffle(group2)


    for j in range(0,3):
        # Board all of the odd rows on the left side
        for i in range(plane[0] - 2, -1, -2):
          group3.append([i, j])
          random.shuffle(group3)


    for j in range(0, 3):
        # Board all of the odd rows on the right side
        for i in range(plane[0] - 2, -1, -2):
          group4.append([i,6 - j])
          random.shuffle(group4)

    for i in range(len(group1)):
        x = (group1[i][0])
        y = (group1[i][1])
        if views == []:
          passengers.append(Passenger(x, y , 'X', len(passengers)))
        else:
          passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))

    for i in range(len(group2)):
        x = (group2[i][0])
        y = (group2[i][1])
        if views == []:
          passengers.append(Passenger(x, y , 'X', len(passengers)))
        else:
          passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))

    for i in range(len(group3)):
        x = (group3[i][0])
        y = (group3[i][1])
        if views == []:
          passengers.append(Passenger(x, y , 'X', len(passengers)))
        else:
          passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))


    for i in range(len(group4)):
        x = (group4[i][0])
        y = (group4[i][1])
        if views == []:
          passengers.append(Passenger(x, y , 'X', len(passengers)))
        else:
          passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))


    return(passengers)   

def zoneRotate(num,plane,views,numgroups):
  seating = []
  for i in range(0, plane[0]):
    w=0
    for j in range(0, plane[1]):
      if((i == 0 or i == plane[0] - 1) and (j == 0 or j == 1 or j == plane[1] - 1)):
        pass
      elif j != middle:
        if j>middle:
          seating.insert(0,[i, j])
        else:
          seating.insert(w,[i,j])
          w=w+1

  passengers = []
  j=math.ceil(plane[0]/numgroups)*(plane[1]-1)
  i=0
  ct=0
  temp=[]
  while i<num:
    k=j
    while k>0 and i<num:
      if len(seating)<j:
        index=len(seating)-1
        coord = seating[index]
        if views == []:
          temp.append(Passenger(coord[0], coord[1], 'X',i))
        else:
          temp.append(gPassenger(coord[0], coord[1], 'X', views[i], i))
      elif (numgroups-ct)%2==0:
        index=0
        coord = seating[index]
        if views == []:
          temp.append(Passenger(coord[0], coord[1], 'X',i))
        else:
          temp.append(gPassenger(coord[0], coord[1], 'X', views[i], i))
      else:
        index=len(seating)-k
        coord = seating[index]
        if views == []:
          temp.append(Passenger(coord[0], coord[1], 'X',i))
        else:
          temp.append(gPassenger(coord[0], coord[1], 'X', views[i], i))
      seating.remove(coord)
      k=k-1
      i=i+1
    random.shuffle(temp)
    for why in range(0,len(temp)):
      passengers.append(temp[why])
    ct=ct+1
    temp.clear()

  return passengers
        
def backToFront(num,plane,views,numgroups):
  passengers = []
  big=[]
  k=0
  size=math.ceil(plane[0]/numgroups)*(plane[1]-1)
  for i in range(0, plane[0]):
    w=0
    for j in range(0, plane[1]):
      if((i == 0 or i == plane[0] - 1) and (j == 0 or j == 1 or j == plane[1] - 1)):
        pass
      elif j != middle:
        if j>middle:
          if views == []:
            big.insert(0,Passenger(i, j,'X',k))
          else:
            big.insert(0,gPassenger(i, j,'X',views[k],k))
        else:
          if views == []:
            big.insert(w,Passenger(i,j,'X',k))
          else:
            big.insert(w,gPassenger(i,j,'X',views[k],k))
          w=w+1
        k=k+1
  thi=size
  temp=[]
  for check in range(0,num):
    if check<num:
      temp.append(big[check])
      thi=thi-1
    if thi==0 or check==num-1:
      random.shuffle(temp)
      for y in range(0,len(temp)):
        passengers.append(temp[y])
#                      print(rows)
#                      print(temp[y].rowNum)
      temp.clear()
      thi=size

  return passengers

def reversePyramid(num, plane, views):
  passengers=[]
  coord =[]
  group1 = []
  group2 = []
  group3 = []
  group4 = []
  group5 = []

  for i in range(0,9):
    for j in range (2,5):
    #first group; about 70 percent of aisle seats are boarded
      if (j == 4 or j == 2):
        group5.append([i,j])
  random.shuffle(group5)

  for i in range(9,23):
  #second group; rest of aisle seats and a little bit of middle column
    for j in range(2,5):
      if (j == 2 or j == 4):
        group4.append([i,j])
    
  for i in range(0,6):
    for j in range(1,6):
      if (j==1 and i != 0):
        group4.append([i,j])
      if(j==5):
        group4.append([i,j])
  random.shuffle(group4)

  for i in range(6,20):
    for j in range(1,6):
      if (j==1 or j==5):
        group3.append([i,j])
                
  for i in range(1,14):
    for j in range(0,7):
      if(j==0 or j==6):
        group3.append([i,j])
  random.shuffle(group3)

  for i in range(20,23):
    for j in range(1,6):
      if (i!=22 and j==1):
        group2.append([i,j])
      if(j==5):
        group2.append([i,j])
                    
  for i in range(14,19):
    for j in range(0,7):
      if(j==0 or j==6):
        group2.append([i,j])
  random.shuffle(group2)

  for i in range (19,22):
    for j in range(0,7):
      if(j==0 or j==6):
        group1.append([i,j])
    random.shuffle(group1)

  for i in range(len(group1)):
    x = (group1[i][0])
    y = (group1[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))

  for i in range(len(group2)):
    x = (group2[i][0])
    y = (group2[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))

  for i in range(len(group3)):
    x = (group3[i][0])
    y = (group3[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))

  for i in range(len(group4)):
    x = (group4[i][0])
    y = (group4[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))
        
  for i in range(len(group5)):
    x = (group5[i][0])
    y = (group5[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))
            
  return passengers

def efficient(num, plane, views):
  passengers=[]
  coord =[]
  group1 = []
  group2 = []
  group3 = []
  group4 = []
  group5 = []

  for i in range(3,17):
    for j in range (2,5):
    #first group; about 70 percent of aisle seats are boarded
      if (j == 4 or j == 2):
        group5.append([i,j])
  random.shuffle(group5)

  for i in range(17,23):
  #second group; rest of aisle seats and a little bit of middle column
    for j in range(2,5):
      if (j == 2 or j == 4):
        group4.append([i,j])
    
  for i in range(3,6):
    for j in range(1,6):
      if (j==1 or j==5):
        group4.append([i,j])
  random.shuffle(group4)
  
  for i in range(6,20):
    for j in range(1,6):
      if (j==1 or j==5):
        group3.append([i,j])
                
  for i in range(3,6):
    for j in range(0,7):
      if(j==0 or j==6):
        group3.append([i,j])
  random.shuffle(group3)
  
  for i in range(20,23):
    for j in range(1,6):
      if (i!=22 and j==1):
        group2.append([i,j])
      if(j==5):
        group2.append([i,j])
                    
  for i in range(6,22):
    for j in range(0,7):
      if(j==0 or j==6):
        group2.append([i,j])
  random.shuffle(group2)
  
  for i in range (1,3):
    for j in range(0,7):
      if(j!=3):
        group1.append([i,j])
  for j in range(2,6):
    if(j!=3):
      group1.append([0,j])
  random.shuffle(group1)
  
  for i in range(len(group1)):
    x = (group1[i][0])
    y = (group1[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))

  for i in range(len(group2)):
    x = (group2[i][0])
    y = (group2[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))

  for i in range(len(group3)):
    x = (group3[i][0])
    y = (group3[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))

  for i in range(len(group4)):
    x = (group4[i][0])
    y = (group4[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))
        
  for i in range(len(group5)):
    x = (group5[i][0])
    y = (group5[i][1])
    if views == []:
      passengers.append(Passenger(x, y , 'X', len(passengers)))
    else:
      passengers.append(gPassenger(x, y , 'X', views[len(passengers)], len(passengers)))
            
  return passengers


def graphicsRun(v, passengers, seating):
  v.timer = 0
  processes = []

  print("\nClick to Start")

  start = False
  while start == False:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        start = True

  finished = False

  while finished == False:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.quit()
        finished = True
    pygame.event.pump()
    processes = []
    for passenger in passengers:
      processes = passenger.update(seating, processes)
    finished = allSeated(passengers)
    v.moveMultiple(processes)

    processes = []

  running = True
  while running == True:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.quit()
        running = False


def setRuns():
  numRuns = 0
  while numRuns < 1:
    try:
      print("\nSelect Number of Runs\n")
      numRuns = int(input())
    except ValueError:
      print("! Invalid Input !")
  return numRuns


def setPassengers(planeDimensions, v, strategy, groups):
  passengers = []
  strat = 0

  if strategy != 0:
    strat = strategy

  while strat > 8 or strat < 1:
    try:
      print("Choose boarding method:\n1:Random\n2:Back to Front\n3:Outside In\n4:Reverse Pyramid\n5:Efficient\n6:Optimal\n7:Zone Rotate\n8:Steffen's Optimal\n")
      strat = int(input())
    except ValueError:
      pass
    if strat > 8 or strat < 1:
      print("\n! Invalid Input !\n")

  if strat == 1:
    if strategy == 0:
      print("--Random--")
    passengers = randomBoarding(capacity, planeDimensions, v)

  elif strat == 2:
    if strategy == 0:
      print("--Back to Front--")

      groups = 0
      while groups <1 or groups > rows:
        try:
          print("\n select number of groups:")
          groups = int(input())
        except ValueError:
          pass
        if groups < 1 or groups > rows:
          print("\n! Invalid Input!\n")

    passengers = backToFront(capacity, planeDimensions, v, groups)

  elif strat == 3:
    if strategy == 0:
      print("--Outside In--")
    passengers = outsideInBoarding(capacity, planeDimensions, v)

  elif strat == 4:
    if strategy == 0:
      print("--Reverse Pyramid--")
    passengers = reversePyramid(capacity, planeDimensions, v)

  elif strat == 5:
    if strategy == 0:
      print("--Efficient--")
    passengers = efficient(capacity, planeDimensions, v)

  elif strat == 6:
    if strategy == 0:
      print("--Optimal--")
    passengers = optimalStrategy(capacity, planeDimensions, v)

  elif strat == 7:
    if strategy == 0:
      print("--Zone Rotate--")
    
      groups = 0
      while groups <1 or groups > rows:
        try:
          print("\n select number of groups:")
          groups = int(input())
        except ValueError:
          pass
        if groups < 1 or groups > rows:
          print("\n! Invalid Input!\n")

    passengers = zoneRotate(capacity, planeDimensions, v, groups)

  elif strat == 8:
    if strategy == 0:
      print("--Steffen's Optimal--")
    passengers = steffensOptimalBoarding(capacity, planeDimensions, v)

  return (passengers,strat,groups)


def quickRun(passengers, seating, numRuns):
  time = 0

  finished = False
  while finished == False:
    for p in passengers:
      p.update(seating)
    time += 1
    finished = allSeated(passengers)

  minutes = math.floor(time/60)
  seconds = time - (minutes*60)
  if seconds <10:
    print("Time: "+str(minutes)+":0"+str(seconds))
  else:
    print("Time: "+str(minutes)+":"+str(seconds))

  return time

def stDev(arr):
  N = len(arr)

  total = 0
  for e in arr:
    total += e

  xBar = math.floor(total/N)

  topSum = 0
  for e in arr:
    topSum += (e-xBar)**2

  s = math.floor((topSum/(N-1))**0.5)

  return (s,xBar)


def runProgram(processes):

  print("\nInitializing Values...\n")

  planeDimensions = [rows, cols]

  numRuns = setRuns()

  strat = 0
  groups = 0
  times = []

  for trial in range(0,numRuns):

    passengers = []

    if numRuns == 1:
      processes = processes
      v = View()
      v.addSprite(capacity)
      passStrat = setPassengers(planeDimensions, v.spriteGroup.sprites(), strat, groups)
      passengers = passStrat[0]
      strat = passStrat[1]
      groups = passStrat[2]
      v.moveMultiple(processes)
    else:
      passStrat = setPassengers(planeDimensions, [], strat, groups)
      passengers = passStrat[0]
      strat = passStrat[1]
      groups = passStrat[2]

    seating = initSeating(rows, cols)

    ct = 0
    numpass = len(passengers)

    if numRuns == 1:
      graphicsRun(v, passengers, seating)
    else:
      times.append(quickRun(passengers, seating, numRuns))


  # To Write to an excel file:
  #fileName = 'times1.xlsx'
  #df = pd.DataFrame(times)
  #df.to_excel(fileName)

  if numRuns != 1:
    stdMean = stDev(times)
    tAve = stdMean[1]
    std = stdMean[0]

    minutes = math.floor(tAve/60)
    seconds = tAve-(minutes*60)
    if seconds < 10:
      print("\nAverage: "+str(minutes)+":0"+str(seconds))
    else:
      print("\nAverage: "+str(minutes)+":"+str(seconds))

    sMinutes = math.floor(std/60)
    sSeconds = std-(sMinutes*60)
    if sSeconds<10:
      print("Standard Deviation: "+str(sMinutes)+":0"+str(sSeconds))
    else:
      print("Standard Deviation: "+str(sMinutes)+":"+str(sSeconds))

  for i in range(0,len(times)):
    times[i] = times[i]/60

  return times


stop = False
manyTimes = []
while stop == False:
  processes = []
  manyTimes.append(runProgram(processes))
  ans = 0
  while ans != 1 and ans != 2:
    try:
      print("\nContinue?\n1. Yes\n2. No")
      ans = int(input())
    except ValueError:
      pass
    if ans != 1 and ans != 2:
      print("\n! Invalid Input !\n")
  if ans == 2:
    stop = True

#To Write to an excel file:
#fileName = 'times5.xlsx'
#df = pd.DataFrame(manyTimes)
#df.to_excel(fileName)

