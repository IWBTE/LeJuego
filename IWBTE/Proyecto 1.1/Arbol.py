import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class Arbol(pygame.sprite.Sprite):
    def __init__ (self,posx,posy,load_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("Arbol.png", "imagenes", alpha=True)
        self.rect = Rect(0,0,10,10)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.time = 0
