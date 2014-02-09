import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

def load_image(nombre, dir_imagen, alpha=False):
    """Funcion que retorna una imagen"""
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print ("Error, no se puede cargar la imagen: ", ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

class Fireball(pygame.sprite.Sprite):
    def __init__(self,posx,posy,_cargaImagen):
        pygame.sprite.Sprite.__init__(self)
        self.distancia = 0
        self.frameActual=1
        self.image = load_image("Fireball/f1.gif", "imagenes", alpha=True)
        self.rect = Rect(0,0,20,20)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.mov = True
        self.ver = True
        self.vel = 2.8

    def atRaul(self, poisoneado):
        if self.rect.colliderect(poisoneado.rect) and not(poisoneado.invencible):
            self.kill()
            self.mov = False
            poisoneado.invencible = True
            return 30
        else:
            return 0

    def cambiarFrame(self):
        if self.mov == True:
            self.frameActual += 1            
            if self.frameActual>5:
                self.frameActual = 1
            a = self.frameActual//3 + 1
            self.image = load_image("Fireball/f"+str(a)+".gif", "imagenes", alpha=True)

    def mover(self,tiempo,objetivo):
        if objetivo.rect.centerx > self.rect.centerx and not(self.ver):
            self.rect.centerx = self.rect.centerx + (self.vel)*(tiempo/30)            
        elif objetivo.rect.centerx < self.rect.centerx and not(self.ver):
            self.rect.centerx = self.rect.centerx - (self.vel)*(tiempo/30)
        if objetivo.rect.centery > self.rect.centery and self.ver:
            self.rect.centery = self.rect.centery + (self.vel)*(tiempo/30)
        elif objetivo.rect.centery < self.rect.centery and self.ver:
            self.rect.centery = self.rect.centery - (self.vel)*(tiempo/30)
            
        self.distancia+=(self.vel)*(tiempo/30)

        if self.rect.centery >= objetivo.rect.centery-10 and self.ver:
            self.ver=False
            self.vel = 7

        if self.distancia>370:
            self.kill()
            self.mov = False
