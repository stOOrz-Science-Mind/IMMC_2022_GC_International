from graphics import *
import numpy as np
import time
from threading import Timer
import math

walk1 = 'Assets/24p/Sprite1.png'
walk2 = 'Assets/24p/Sprite2.png'
walk3 = 'Assets/24p/Sprite1.png'
walk4 = 'Assets/24p/Sprite3.png'
nothing = 'Assets/24p/Nothing.png'
stowR1 = 'Assets/24p/stowR1.png'
stowR2 = 'Assets/24p/stowR2.png'
stowR3 = 'Assets/24p/stowR3.png'
stowR4 = 'Assets/24p/stowR2.png'
stowL1 = 'Assets/24p/stowL1.png'
stowL2 = 'Assets/24p/stowL2.png'
stowL3 = 'Assets/24p/stowL3.png'
stowL4 = 'Assets/24p/stowL2.png'
walk = [walk1, walk2, walk3, walk4]
stowR = [stowR1, stowR2, stowR3, stowR4]
stowL = [stowL1, stowL2, stowL3, stowL4]
sitting = 'Assets/24p/Sitting.png'

tileHeight = 24  # height of a tile (passenger, seat, etc) in pixels
speed = 1  # number of tiles a passenger can move through in 1 second without interference


class View():
    def __init__(self, columns, rows):
        self.col = columns
        self.row = rows
        self.width = tileHeight * columns
        self.height = tileHeight * columns + tileHeight
        self.win = self.createWindow()
        self.passengers = []
        self.time = 0
        self.time0 = 0
        self.clock = Text(Point(self.width - 10, 10), "0")
        self.clock.draw(self.win)

    def createWindow(self):

        # Establishes static tiles representing the plane (seats, aisle, etc.)

        win = GraphWin("Airplane Boarding", tileHeight * self.col, tileHeight * self.row + tileHeight)
        for i in range(0, self.row + 1):
            for j in range(0, self.col):
                if j == math.floor(self.col / 2):
                    self.drawImg(win, j, i, 'Assets/24p/Aisle.png')
                elif i == 0:
                    self.drawImg(win, j, i, 'Assets/24p/Empty.png')
                else:
                    self.drawImg(win, j, i, 'Assets/24p/Seat.png')
        return win

    def drawImg(self, win, x, y, name):

        # Prints the image of name (name) at x,y corresponding to tile coordinates, not pixel coordinates

        img = Image(Point((tileHeight * x) + tileHeight / 2, (tileHeight * y) + tileHeight / 2), name)
        img.draw(win)

    def drawPass(self, win, p, name):

        # Prints image of name (name) at the x,y coordinates of a passenger p

        img = Image(Point(p.x, p.y), name)
        img.draw(win)
        return img

    def addPass(self, num):

        # Instantiates a new passenger at the default starting location - the top of the aisle

        for i in range(0, num):
            self.passengers.append(Passenger(self.width / 2, -1 * (tileHeight / 2) - (tileHeight * (2 / 3)), self.win))
            self.drawPass(self.win, self.passengers[-1], nothing)

    def moveMultiple(self, processes):

        # Takes a list of processes (a passenger and a movement/change)
        # Executes all changes simultaneously without the use of threading at (speed) fps

        for i in range(0, 8):
            for j in range(0, len(processes)):
                if processes[j][1] == 'down':
                    self.passengers[processes[j][0]].smallDown(i % 4)
                elif processes[j][1] == 'up':
                    self.passengers[processes[j][0]].smallUp(i % 4)
                elif processes[j][1] == 'right':
                    self.passengers[processes[j][0]].smallRight(i % 4)
                elif processes[j][1] == 'left':
                    self.passengers[processes[j][0]].smallLeft(i % 4)
                elif processes[j][1] == 'stowR':
                    self.passengers[processes[j][0]].stow(i % 4, "r")
                elif processes[j][1] == 'stowL':
                    self.passengers[processes[j][0]].stow(i % 4, "l")
                elif processes[j][1] == 'nothingL':
                    self.passengers[processes[j][0]].smallLeft(i%4)
                elif processes[j][1] == 'nothingR':
                    self.passengers[processes[j][0]].smallRight(i%4)
                else:
                    self.passengers[processes[j][0]].sitDown()
            time.sleep(speed / 8)
        self.updateTime()

    def startTime(self):
        self.time0 = math.floor(time.clock())

    def updateTime(self):
        self.time = math.floor(time.clock())
        self.clock.setText(str(self.time))


class Passenger():
    def __init__(self, xPos, yPos, win):
        self.win = win
        self.x = xPos
        self.y = yPos
        self.sprite = Image(Point(self.x, self.y), nothing)
        self.sitting = False

    def drawPass(self, name):

        # Draws a passenger to win at its x and y coordinates
        # takes name (string) to indicate its sprite

        if(self.y <= -(tileHeight / 4)):
            name = nothing
        img = Image(Point(self.x, self.y), name)
        img.draw(self.win)
        return img

    def smallWalk(self, x, y, frame):

        # Walks in a direction, cycling through the walking animation
        # Responsible for one fourth of a walk cycle or one eighth of a tileHeight movement
        # x and y are either 0, 1 or -1, indicating positive or negative movement on the axis.
        # If x/y is not 0, the other must be 0

        #self.sprite.undraw()
        self.x += (tileHeight * x) / 8
        self.y += (tileHeight * y) / 8
        #self.sprite = self.drawPass(walk[frame])

    # Following methods call smallWalk for different directions

    def smallDown(self, frame):
        self.smallWalk(0, 1, frame)

    def smallUp(self, frame):
        self.smallWalk(0, -1, frame)

    def smallRight(self, frame):
        self.smallWalk(1, 0, frame)

    def smallLeft(self, frame):
        self.smallWalk(-1, 0, frame)

    def stow(self, frame, dir):

        # Cycles through stowing animation, alters based on side of aisle they must stow their bag

        self.sprite.undraw()
        if dir == 'r':
            self.sprite = self.drawPass(stowR[frame])
        else:
            self.sprite = self.drawPass(stowL[frame])

    def sitDown(self):
        if self.sitting == False:
            self.sprite.undraw()
            self.y += (tileHeight * (2 / 3))
            self.sprite = self.drawPass(sitting)
            self.sitting = True


# v.win.getMouse()  # Waits for mouseclick to continue
# v.win.close()    # Closes window
