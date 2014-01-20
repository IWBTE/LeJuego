import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class Heart(pygame.sprite.Sprite):
    def __init__(self,posx,posy,_cargaImagen):
        self.distancia = 0
        self.cargaImagen = _cargaImagen
        self.image = self.cargaImagen("Corazon/c1.gif", "imagenes", alpha=True)
        self.rect = rect(0,0,10,20)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.mov = True
