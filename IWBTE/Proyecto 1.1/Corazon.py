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

class Corazon(pygame.sprite.Sprite):
    def __init__(self,posx,posy,_cargaImagen):
        pygame.sprite.Sprite.__init__(self)
        self.distancia = 0
        self.frameActual=1
        self.image = load_image("Corazon/c1.gif", "imagenes", alpha=True)
        self.rect = Rect(0,0,10,20)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.mov = True

    def flechazo(self, baleado):
        if self.rect.colliderect(baleado.rect):
            self.kill()
            self.mov = False
            baleado.invencible = True
            return True

    def cambiarFrame(self):
        if self.mov == True:
            self.frameActual += 1            
            if self.frameActual>5:
                self.frameActual = 1
            a = self.frameActual//3 + 1
            self.image = load_image("Corazon/c"+str(a)+".gif", "imagenes", alpha=True)

    def mover(self,tiempo,objetivo):
        if objetivo.rect.centerx > self.rect.centerx:
            self.rect.centerx = self.rect.centerx + 3.6*(tiempo/30)            
        elif objetivo.rect.centerx < self.rect.centerx:
            self.rect.centerx = self.rect.centerx - 3.6*(tiempo/30)
        if objetivo.rect.centery > self.rect.centery:
            self.rect.centery = self.rect.centery + 3.6*(tiempo/30)
        elif objetivo.rect.centery < self.rect.centery:
            self.rect.centery = self.rect.centery - 3.6*(tiempo/30)
            
        self.distancia+=3.4*(tiempo/30)

        if self.distancia>190:
            self.kill()
            self.mov = False