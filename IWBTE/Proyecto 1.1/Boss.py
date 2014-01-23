import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class Boss(pygame.sprite.Sprite):
    def __init__(self, _loadImage):
        pygame.sprite.Sprite.__init__(self)
        self.loadImage = _loadImage
        self.frameActual=1
        self.rect = Rect(0,0,20,30)
        self.rect.centerx=310
        self.rect.centery = 0
        self.invencible = True
        self.introduccion = 0

class Montes(Boss):
    def __init__(self, _loadImage):
        Boss.__init__(self,_loadImage)
        self.hp = 500
        self.image = self.loadImage("Montes/d1.gif","imagenes",alpha=False)

    def cambiarFrame(self):
        self.frameActual+=1
        if self.frameActual>8:
            self.frameActual=1
        

    def mover(self,tiempo):
        if self.introduccion<=3000:
            self.introduccion+=tiempo
        if self.introduccion>=3000:
            self.invencible = False
        if self.rect.centery<=100:
            self.rect.centery += 3*(tiempo/30)
            a = self.frameActual//3 + 1
            self.image = self.loadImage("Montes/d"+str(a)+".gif","imagenes",alpha=False)
        if self.introduccion > 3000:
            pass




