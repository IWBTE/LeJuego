import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class Arbol(pygame.sprite.Sprite):
    def __init__ (self,posx,posy,_loadImage):
        pygame.sprite.Sprite.__init__(self)
        self.loadImage = _loadImage
        self.image = self.loadImage("Arbol.png", "imagenes", alpha=True)
        self.rect = Rect(0,0,10,20)
        self.rect.centerx = posx
        self.rect.centery = posy
