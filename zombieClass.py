#!/usr/bin/env python3
import pygame
from MyPRNG import MyPRNG

class Zombie(pygame.sprite.Sprite):

    def __init__(self, sprite, startSpot, endSpot, waypointList):
        # call parent's constructor MUST BE HERE
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("zombieWithAxe.png")
        self.rect = self.image.get_rect()
        self.rect.x = startSpot[0]
        self.rect.y = startSpot[1]

        # import the path to follow
        self.path = waypointList
        self.path.append(endSpot)

    # not actually used in game anymore
    # navigated zombies toward player
    def pathFind(self, zombieRect, playerRect):

        if self.rect.x > playerRect.x:
            self.rect.x += -1
        elif self.rect.x < playerRect.x:
            self.rect.x += 1
        else:
            self.rect.x += 0

        if self.rect.y > playerRect.y:
            self.rect.y += -1
        elif self.rect.y < playerRect.y:
            self.rect.y += 1
        else:
            self.rect.y += 0

    # moves zombies toward each waypoint
    def move(self):
        if len(self.path) == 0:
            print("path empty!")
            return

        # if first element x and first element y of path == zombie x,y, delete first waypoint
        if self.path[0][0] == self.rect.x and self.path[0][1] == self.rect.y:
            # delete the first waypoint of the path
            self.path = self.path[1:]

        # move to the first waypoint currently in list
        if self.rect.x > self.path[0][0]:
            self.rect.x += -1
        elif self.rect.x < self.path[0][0]:
            self.rect.x += 1
        else:
            self.rect.x += 0

        if self.rect.y > self.path[0][1]:
            self.rect.y += -1
        elif self.rect.y < self.path[0][1]:
            self.rect.y += 1
        else:
            self.rect.y += 0

    def getPostion(self):
        print(self.rect.x, self.rect.y)
