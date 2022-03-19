from graphics import *
import numpy as np
import time
from threading import Timer
import math
import pygame
from typing import Tuple

walk1 = pygame.image.load('Assets/24p/Sprite1.png')
walk2 = pygame.image.load('Assets/24p/Sprite2.png')
walk3 = pygame.image.load('Assets/24p/Sprite1.png')
walk4 = pygame.image.load('Assets/24p/Sprite3.png')
nothing = pygame.image.load('Assets/24p/Nothing.png')
stowR1 = pygame.image.load('Assets/24p/stowR1.png')
stowR2 = pygame.image.load('Assets/24p/stowR2.png')
stowR3 = pygame.image.load('Assets/24p/stowR3.png')
stowR4 = pygame.image.load('Assets/24p/stowR2.png')
stowL1 = pygame.image.load('Assets/24p/stowL1.png')
stowL2 = pygame.image.load('Assets/24p/stowL2.png')
stowL3 = pygame.image.load('Assets/24p/stowL3.png')
stowL4 = pygame.image.load('Assets/24p/stowL2.png')
walk = [walk1, walk2, walk3, walk4]
stowR = [stowR1, stowR2, stowR3, stowR4]
stowL = [stowL1, stowL2, stowL3, stowL4]
sitting = pygame.image.load('Assets/24p/Sitting.png')
aisle = pygame.image.load('Assets/24p/Aisle.png')
empty = pygame.image.load('Assets/24p/Empty.png')
seat = pygame.image.load('Assets/24p/Seat.png')
lWing = pygame.image.load('Assets/24p/leftWing.png')
rWing = pygame.image.load('Assets/24p/rightWing.png')
bg = [aisle, empty, seat, lWing, rWing]

tileHeight = 24
rows = 23
cols = 7
wingWidth = (((rows + 1) * tileHeight) - (cols * tileHeight)) / 2
speed = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Passenger(pygame.sprite.Sprite):

    def __init__(self):
        super(Passenger, self).__init__()
        self.images = walk

        self.index = 0
        self.image = self.images[self.index]

        self.isSitting = False

        self.x = wingWidth + (math.floor(cols / 2) * tileHeight)
        self.y = (-5 / 3) * tileHeight

        self.rect = pygame.Rect(self.x, self.y, tileHeight, tileHeight)

        self.speed = 1
        self.skip = False

    def update(self):
        if self.rect.y < -1 * tileHeight / 2:
            self.index = 0
            self.image = nothing
        elif self.isSitting == False:

            self.index += 1

            if self.index > 3:
                self.index = 0
            self.image = self.images[self.index]

    def stow(self, dir):
        if dir == 'r':
            self.images = stowR
        else:
            self.images = stowL

    def sit(self):
        if self.isSitting == False:
            self.index = 0
            self.images = [sitting]
            self.rect.y += (2 / 3) * tileHeight
            self.image = self.images[self.index]
            while (self.rect.x - wingWidth) % tileHeight != 0:
                if (self.rect.x - wingWidth) % tileHeight > (tileHeight / 2):
                    self.rect.x += 1
                else:
                    self.rect.x -= 1
            self.isSitting = True

    def move(self, char):
        if char == 'down':
            self.moveDown()
        elif char == 'right':
            self.moveRight()
        elif char == 'left':
            self.moveLeft()
        elif char == 'up':
            self.moveUp()
        elif char == 'stowL':
            self.stow('l')
        elif char == 'stowR':
            self.stow('r')
        elif char == 'sit':
            self.sit()
        elif char == 'half':
            self.speed = 0
        elif char == 'double':
            self.speed = 1

    def moveDown(self):
        self.images = walk
        self.rect.y += tileHeight / 8

    def moveRight(self):
        self.images = walk
        if self.speed == 1 or self.skip == False:
            self.rect.x += tileHeight / 8
            if self.speed != 1:
                self.skip = True
        else:
            self.skip == False

    def moveLeft(self):
        self.images = walk
        if self.speed == 1 or self.skip == False:
            self.rect.x -= tileHeight / 8
            if self.speed != 1:
                self.skip = True
        else:
            self.skip == False

    def moveUp(self):
        self.images = walk
        self.rect.y -= tileHeight / 8

class Tile(pygame.sprite.Sprite):

    def __init__(self, ind, pos):

            # ind corresponds to which background tile it is:
            # 0 = aisle
            # 1 = empty
            # 2 = seat
            # 3 = left wing
            # 4 = right wing
            # pos corresponds to where the tile is on the background

        super(Tile, self).__init__()
        self.images = bg
        self.index = ind
        self.image = self.images[self.index]
        if ind < 3:
            self.height = tileHeight
        else:
            self.height = tileHeight * (rows + 1)
        self.rect = pygame.Rect(pos[0], pos[1], self.height, self.height)


class Window(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Window, self).__init__()
        self.rect = pygame.Rect(tileHeight * width / 2, tileHeight * height / 2,
                                tileHeight * width, tileHeight * height)
        self.tiles = []
        self.index = 0
        self.images = [nothing]
        self.image = self.images[self.index]

        for y in range(0, height):
            for x in range(0, width):

                pos = [wingWidth + (x * tileHeight), y * tileHeight]
                if x == math.floor(width / 2):
                    self.tiles.append(Tile(0, pos))
                elif (y == 0) or ((y == 1 or y == height - 1) and (x == 0 or x == 1 or x == width - 1)):
                    self.tiles.append(Tile(1, pos))
                else:
                    self.tiles.append(Tile(2, pos))

        self.tiles.append(Tile(3, [0, 0]))
        self.tiles.append(Tile(4, [wingWidth + (cols * tileHeight), 0]))

    def update(self):
        pass


class View():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode([int((rows + 1) * tileHeight), int((rows + 1) * tileHeight)])

        pygame.display.set_caption('Airplane Boarding')
        self.win = Window(cols, rows + 1)

        self.tileGroup = pygame.sprite.Group()
        for tile in self.win.tiles:
            self.tileGroup.add(tile)
        self.tileGroup.draw(self.screen)

        self.spriteGroup = pygame.sprite.Group()

        self.timer = 0

        self.font = pygame.font.Font('freesansbold.ttf', tileHeight)
        self.text = self.font.render(str(self.timer), True, WHITE, BLACK)
        self.textRect = self.text.get_rect()
        self.textRect.center = (wingWidth / 2, tileHeight / 2)

        self.clock = pygame.time.Clock()

    def addSprite(self, num):
        for i in range(0, num):
            self.spriteGroup.add(Passenger())

    def update(self):
        self.spriteGroup.update()
        self.tileGroup.draw(self.screen)
        self.spriteGroup.draw(self.screen)

        secs = self.timer % 60
        if secs < 10:
            secStr = str("0" + str(secs))
        else:
            secStr = str(secs)

        self.text = self.font.render(str(math.floor(self.timer / 60)) + ":" + secStr, True, WHITE, BLACK)
        self.textRect = self.text.get_rect()
        self.textRect.center = (wingWidth / 2, tileHeight / 2)
        self.screen.blit(self.text, self.textRect)

        pygame.display.update()
        # self.clock.tick(8)

    def moveMultiple(self, processes):
        for i in range(0, 8):
            for p in processes:
                self.spriteGroup.sprites()[p[0]].move(p[1])
            self.update()
        self.timer += 1


def main():

    v = View()

    v.addSprite(2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    quit()

        v.update()


# main()
