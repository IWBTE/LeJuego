import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class Enemy(pygame.sprite.Sprite):
    def __init__(self, _loadImage):
        pygame.sprite.Sprite.__init__(self)
        self.loadImage = _loadImage
        self.frameActual=1   
        num = randint(0,1)
        self.rect = Rect(0,0,20,30)
        self.rect.centerx=610
        self.rect.centery=480*num
        self.vivo = True

    def colisionConPersonaje(self, machucao):
        if self.rect.colliderect(machucao.rect) and not(machucao.invencible):
            machucao.invencible=True
            return True

    def hustonTenemosProblemas(self, etapa):
        for i in etapa.lovers:
            if self.rect.colliderect(i.rect) and not(self.rect is i.rect):
                return True
        for j in etapa.zorrones:
            if self.rect.colliderect(j.rect) and not(self.rect is j.rect):
                return True
        return False

    def mover(self, objetivo, reloj, etapa):
        #Forgive me for this sin...
        if objetivo.rect.centerx - self.rect.centerx >= 0:
            self.image = self.loadImage(self.path+"r"+str(self.frameActual)+".gif","imagenes",alpha=False)            
            respaldo = self.rect.centerx
            self.rect.centerx += self.velocidad*(reloj/30)
            if self.hustonTenemosProblemas(etapa):
                self.rect.centerx = respaldo
        else:
            self.image = self.loadImage(self.path+"l"+str(self.frameActual)+".gif","imagenes",alpha=False)            
            respaldo = self.rect.centerx
            self.rect.centerx -= self.velocidad*(reloj/30)
            if self.hustonTenemosProblemas(etapa):
                self.rect.centerx = respaldo

        if objetivo.rect.centery - self.rect.centery >= 0:
            if objetivo.rect.centery - self.rect.centery >= 10:
                self.image = self.loadImage(self.path+"d"+str(self.frameActual)+".gif","imagenes",alpha=False)
            respaldo = self.rect.centery
            self.rect.centery += self.velocidad*(reloj/30)
            if self.hustonTenemosProblemas(etapa):
                self.rect.centery = respaldo
        else:
            if objetivo.rect.centery - self.rect.centery <= -10:
                self.image = self.loadImage(self.path+"u"+str(self.frameActual)+".gif","imagenes",alpha=False)
            respaldo = self.rect.centery
            self.rect.centery -= self.velocidad*(reloj/30)
            if self.hustonTenemosProblemas(etapa):
                self.rect.centery = respaldo

    def cambiarFrame(self):
        self.frameActual+=1
        if self.frameActual>3:
            self.frameActual=1


class Zorron(Enemy):
    def __init__(self,_loadImage):
        Enemy.__init__(self,_loadImage)
        self.image = self.loadImage("Zorron/Frames/l1.gif", "imagenes", alpha=True)
        self.path = "Zorron/Frames/"
        self.velocidad = 2.3
        self.hp = 50