#!/usr/bin/env python3
import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, sprite, x, y):
        # call parent's constructor MUST BE HERE
        pygame.sprite.Sprite.__init__(self)
        #super(Player, self).__init__()
        # need to fix how this is implemented
        self.image = pygame.image.load(sprite)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def getPostion(self):
        print(self.rect.x, self.rect.y)

    def shoot(self, bulletGroup):
        # create new Bullet object
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        # add bullet to bulletGroup
        bulletGroup.add(bullet)
