import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class EnergyDrink(pygame.sprite.Sprite):
    def __init__ (self,posx,posy,load_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("Drink.gif", "imagenes", alpha=True)
        self.rect = Rect(0,0,10,10)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.bebible = True
        self.time = 0

    def africano(self,jugador):
        if self.rect.colliderect(jugador.rect):
            self.kill()
            self.bebible = False
            return True
    
    def tomameODejame(self,tiempo):
        self.time += tiempo
        if self.time>=5000:
            self.bebible = False
            self.kill()
