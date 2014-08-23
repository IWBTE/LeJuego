import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class HPB(pygame.sprite.Sprite):
    def __init__(self,_cargar, foco):
        pygame.sprite.Sprite.__init__(self)
        self.cargar = _cargar
        self.image = self.cargar("BarraHPB/l100.png", "imagenes", alpha = True)
        self.rect = self.image.get_rect()
        self.foco = foco
        self.rect.centerx=self.foco.rect.centerx
        self.rect.centery=self.foco.rect.centery+40

    def actualizar(self,boss):
        daHP = int(floor(boss.hp))
        self.image = self.cargar("BarraHPB/l"+str(daHP)+".png", "imagenes", alpha = True)
        self.rect.centerx=self.foco.rect.centerx
        self.rect.centery=self.foco.rect.centery+40