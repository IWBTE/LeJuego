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
        self.hp = 150
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
            self.image = self.loadImage("Montes/d"+str(a)+".gif","imagenes",alpha=False)
        if self.introduccion > 3000:
            if self.rect.centerx <10:
                self.velocidad = 4
                self.lugar = "r"
            if self.rect.centerx > 600:
                self.velocidad = -4
                self.lugar = "l"
            self.rect.centerx += self.velocidad*(tiempo/30)
            a = self.frameActual//3 + 1
            self.image = self.loadImage("Montes/"+self.lugar+str(a)+".gif","imagenes",alpha=False)

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
        self.hp = 200
        self.image = self.loadImage("Dissett/d1.gif","imagenes",alpha=False)
        self.velocidad = -7
        self.lugar = "l"
        self.lastAt = 0
        self.Fireball = 0

    def cambiarFrame(self):
        self.frameActual+=1
        if self.frameActual>8:
            self.frameActual=1
        

    def mover(self, objetivo, reloj, etapa):
        a = self.frameActual//3 + 1
        if objetivo.rect.centerx - self.rect.centerx >= 0:
            self.image = self.loadImage(self.path+"r"+str(a)+".gif","imagenes",alpha=False)            
            respaldo = self.rect.centerx
            self.rect.centerx += self.velocidad*(reloj/30)
            if self.hustonTenemosProblemas(etapa):
                self.rect.centerx = respaldo
        else:
            self.image = self.loadImage(self.path+"l"+str(a)+".gif","imagenes",alpha=False)            
            respaldo = self.rect.centerx
            self.rect.centerx -= self.velocidad*(reloj/30)
            if self.hustonTenemosProblemas(etapa):
                self.rect.centerx = respaldo

        if objetivo.rect.centery - self.rect.centery >= 0:
            if objetivo.rect.centery - self.rect.centery >= 10:
                self.image = self.loadImage(self.path+"d"+str(a)+".gif","imagenes",alpha=False)
            respaldo = self.rect.centery
            self.rect.centery += self.velocidad*(reloj/30)
            if self.hustonTenemosProblemas(etapa):
                self.rect.centery = respaldo
        else:
            if objetivo.rect.centery - self.rect.centery <= -10:
                self.image = self.loadImage(self.path+"u"+str(a)+".gif","imagenes",alpha=False)
            respaldo = self.rect.centery
            self.rect.centery -= self.velocidad*(reloj/30)
            if self.hustonTenemosProblemas(etapa):
                self.rect.centery = respaldo


       
