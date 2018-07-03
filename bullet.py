#!/usr/bin/env python3
import pygame

BLACK = (0, 0, 0)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((5,5))
        self.image = pygame.image.load("bombSmall.png")
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        #self.speed = -10

    def update(self):
        #self.rect.x += self.speed
        if self.rect.bottom < 0:
            self.kill()
