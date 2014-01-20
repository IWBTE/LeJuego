import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

#Mis modulos
from Menu import Menu
from Etapa import Etapa

#Constantes

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


#Mis funciones

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





def main():
    pygame.init()
    
    #Creamos la ventana

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("VichoPLS")

    #El reloj
    clock = pygame.time.Clock()

    #Ejecutamos el Menu

    miMenu = Menu(load_image,clock,screen)
    miMenu.ejecutarMenu()

    #Ejecutamos la Etapa

    miEtapa = Etapa(load_image,clock,screen)
    miEtapa.ejecutarEtapa("leJuego")

    pygame.mixer.quit()
    print "GG"

if __name__ == "__main__":
    main()
