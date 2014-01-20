import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class Personaje(pygame.sprite.Sprite):
    def __init__(self, _cargaImagen):
        pygame.sprite.Sprite.__init__(self)
        self.frameActual = 1
        self.asesinatos = 0
        self.hp = 100
        self.cargaImagen = _cargaImagen
        self.image = self.cargaImagen("Vicho/Frames/r1.gif", "imagenes", alpha=True)
        self.rect = Rect(0,0,15,30)
        self.rect.centerx = 100
        self.rect.centery = 240
        self.retrasoBalas = 0
        self.invencible = False
        self.ultimoHit = 0
        self.vivo = True

    def margen(self):
        """Controla que el PJ no se salga"""
        if self.rect.bottom >= 470:
            self.rect.bottom = 470
        elif self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= 630:
            self.rect.right = 630

    def poderDisparar(self,leReloj):
        if self.retrasoBalas>=1:
            self.retrasoBalas+=leReloj
        if self.retrasoBalas>=651:
            self.retrasoBalas=0

    def invencibilidad(self,tiempo):
        if self.invencible == True:
            self.ultimoHit += tiempo
        if self.ultimoHit >= 2000:
            self.ultimoHit = 0
            self.invencible = False

    def moverArriba(self, clock):
        self.rect.centery -= 3*(clock/30)
    
    def moverAbajo(self, clock):
        self.rect.centery += 3*(clock/30)

    def moverDerecha(self, clock):
        self.rect.centerx += 3*(clock/30)

    def moverIzquierda(self, clock):
        self.rect.centerx -= 3*(clock/30)

    def actualizarFrame(self,dir):
        """Actualiza el frame"""
        self.frameActual+=1
        if self.frameActual>=9:
            self.frameActual = 1
        num = (self.frameActual//3)+1
        self.image = self.cargaImagen("Vicho/Frames/"+dir+str(num)+".gif","imagenes",alpha = True)
