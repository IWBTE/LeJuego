import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor
from Serpiente import Serpiente
from Fireball import Fireball
from Laining import Laining

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

    def choque(self,machucao):
        if self.rect.colliderect(machucao.rect) and not(machucao.invencible):
            machucao.invencible=True
            return True

class Montes(Boss):
    def __init__(self, _loadImage):
        Boss.__init__(self,_loadImage)
        self.hp = 100
        self.image = self.loadImage("Montes/d1.gif","imagenes",alpha=False)
        self.velocidad = -4
        self.lugar = "l"
        self.lastAt = 0
        self.Fireball = 0

    def cambiarFrame(self):
        self.frameActual+=1
        if self.frameActual>8:
            self.frameActual=1
        
    def mover(self,tiempo):
        self.cambiarFrame()
        if self.introduccion<=3000:
            self.introduccion+=tiempo
        if self.introduccion>=3000 and self.invencible:
            self.invencible = False
        if self.rect.centery<=100:
            self.rect.centery += 3*(tiempo/30)
            a = self.frameActual//3 + 1
            self.image = self.loadImage("Montes/d"+str(a)+".gif","imagenes",alpha=True)
        if self.introduccion > 3000:
            if self.rect.centerx <10:
                self.velocidad = 4
                self.lugar = "r"
            if self.rect.centerx > 600:
                self.velocidad = -4
                self.lugar = "l"
            self.rect.centerx += self.velocidad*(tiempo/30)
            a = self.frameActual//3 + 1
            self.image = self.loadImage("Montes/"+self.lugar+str(a)+".gif","imagenes",alpha=True)

    def atacar(self,tiempo, objetivo,etapa):
        self.lastAt+=tiempo
        self.Fireball+=tiempo
        if self.lastAt>=1800:
            self.lastAt = 0
            etapa.proyJefe.append(Serpiente(self.rect.centerx,self.rect.centery,self.loadImage))
        if self.Fireball>=7500:
            self.Fireball=0
            etapa.proyJefe.append(Fireball(self.rect.centerx,self.rect.centery,self.loadImage))

class Dissett(Boss):
    def __init__(self, _loadImage):
        Boss.__init__(self,_loadImage)
        self.hp = 100
        self.image = self.loadImage("Dissett/d1.gif","imagenes",alpha=True)
        self.velocidad = -2.5
        self.lugar = "l"
        self.lastAt = 0
        self.rasho = 0
        self.flash = 0
        self.rage = 0

    def cambiarFrame(self):
        self.frameActual+=1
        if self.frameActual>8:
            self.frameActual=1
        

    def mover(self,tiempo):
        self.cambiarFrame()
        self.flash += tiempo
        if self.flash >= 6000:
            self.flash = 0
            if self.rect.centery<200:
                self.rect.centery = 350
            else:
                self.rect.centery = 100
        if self.introduccion<=3000:
            self.introduccion+=tiempo
        if self.introduccion>=3000 and self.invencible:
            self.invencible = False
        if self.rect.centery<=100:
            self.rect.centery += 3*(tiempo/30)
            a = self.frameActual//3 + 1
            self.image = self.loadImage("Dissett/d"+str(a)+".gif","imagenes",alpha=False)
        if self.introduccion > 3000:
            if self.rect.centerx <10:
                self.velocidad = 2.5
                self.lugar = "r"
            if self.rect.centerx > 600:
                self.velocidad = -2.5
                self.lugar = "l"
            self.rect.centerx += self.velocidad*(tiempo/30)
            a = self.frameActual//3 + 1
            self.image = self.loadImage("Dissett/"+self.lugar+str(a)+".gif","imagenes",alpha=False)

    
    def atacar(self,tiempo, objetivo,etapa):
        self.lastAt+=tiempo
        self.rasho+=tiempo
        self.rage += tiempo
        if self.rage >= 10000:
            if self.rasho>=500:
                self.rasho=0
                if self.rect.centery <200:
                    etapa.proyJefe.append(Laining(self.rect.centerx,self.rect.centery,self.loadImage,'r'))
                else:
                    etapa.proyJefe.append(Laining(self.rect.centerx,self.rect.centery,self.loadImage,'u'))
                if self.rage> 12000:
                    self.rage = 0
            
        if self.rasho>=1800:
            self.rasho=0
            if self.rect.centery <200:
                etapa.proyJefe.append(Laining(self.rect.centerx,self.rect.centery,self.loadImage,'r'))
            else:
                etapa.proyJefe.append(Laining(self.rect.centerx,self.rect.centery,self.loadImage,'u'))


       
