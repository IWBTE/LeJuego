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

class BolaFuego(pygame.sprite.Sprite):
    def __init__(self, vichopls,dir):
        pygame.sprite.Sprite.__init__(self)
        self.frameActual = 1
        self.recorrido = 0
        self.image = load_image("Fireball/f1.gif", "imagenes", alpha=True)
        self.rect = Rect(0,0,10,10)
        self.rect.centerx =vichopls.rect.centerx
        self.rect.centery =vichopls.rect.centery
        self.dir = dir
        self.mov = True


        #Instanciacion y llenado del diccionario
        self.movimiento = dict()
        self.movimiento[""] = self.right
        self.movimiento["u"] = self.up
        self.movimiento["d"] = self.down
        self.movimiento["l"] = self.left
        self.movimiento["r"] = self.right
        self.movimiento["ur"] = self.upRight
        self.movimiento["dr"] = self.downRight
        self.movimiento["dl"] = self.downLeft
        self.movimiento["ul"] = self.upLeft

    def tunazo(self, baleado):
        if self.rect.colliderect(baleado.rect):
            return True

    def up(self,reloj):
        if self.recorrido < 250:
            self.recorrido += 6.5*(reloj/30)
            self.rect.centery -= 6.5*(reloj/30)
        else:
            self.kill()
            self.mov = False

    def down(self,reloj):
        if self.recorrido < 250:
            self.recorrido += 6.5*(reloj/30)
            self.rect.centery += 6.5*(reloj/30)
        else:
            self.kill()
            self.mov = False

    def right(self,reloj):
        if self.recorrido < 250:
            self.recorrido += 6.5*(reloj/30)
            self.rect.centerx += 6.5*(reloj/30)
        else:
            self.kill()
            self.mov = False

    def left(self,reloj):
        if self.recorrido < 250:
            self.recorrido += 6.5*(reloj/30)
            self.rect.centerx -= 6.5*(reloj/30)
        else:
            self.kill()
            self.mov = False

    def upRight(self, reloj):
        self.up(reloj)
        self.right(reloj)

    def downRight(self,reloj):
        self.down(reloj)
        self.right(reloj)

    def downLeft(self,reloj):
        self.down(reloj)
        self.left(reloj)

    def upLeft(self,reloj):
        self.up(reloj)
        self.left(reloj)

    def cambiarFrame(self):
        if self.mov == True:
            self.frameActual += 1            
            if self.frameActual>5:
                self.frameActual = 1
            a = self.frameActual//3 + 1
            self.image = load_image("Fireball/f"+str(a)+".gif", "imagenes", alpha=True)
            
    #La funcion mover paso de tener muchas lineas a solo una. Todo auspiciado por Pyhton, yey!
    def mover(self, reloj):
        (self.movimiento[self.dir])(reloj)
