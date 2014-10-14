import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class MP(pygame.sprite.Sprite):
    def __init__(self,_cargar):
        pygame.sprite.Sprite.__init__(self)
        self.cargar = _cargar
        self.image = self.cargar("Barra Mana/b100.gif", "imagenes", alpha = True)
        self.rect = self.image.get_rect()
        self.rect.centerx=500
        self.rect.centery=20

    def actualizar(self,jugador):
        daMP = int(floor(jugador.mp))
        if daMP<=0:
            daMP=0
        if daMP>100:
            daMP=100
        self.image = self.cargar("Barra Mana/b"+str(daMP)+".gif", "imagenes", alpha = True)