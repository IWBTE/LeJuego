import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class HP(pygame.sprite.Sprite):
    def __init__(self,_cargar):
        pygame.sprite.Sprite.__init__(self)
        self.cargar = _cargar
        self.image = self.cargar("Barra HP/h10.gif", "imagenes", alpha = True)
        self.rect = self.image.get_rect()
        self.rect.centerx=115
        self.rect.centery=20

    def actualizar(self,jugador):
        daHP = int(floor(jugador.hp))
        if daHP<=0:
            daHP=0
        if daHP>100:
            daHP=100
        self.image = self.cargar("Barra HP/h"+str(daHP)+".gif", "imagenes", alpha = True)