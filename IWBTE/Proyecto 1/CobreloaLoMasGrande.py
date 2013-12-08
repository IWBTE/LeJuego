import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "imagenes"

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):
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


# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:




class Bala(pygame.sprite.Sprite):
    def __init__(self, vichopls,imag,dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(imag, IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.x0 = vichopls.rect.centerx
        self.y0 = vichopls.rect.centery
        self.rect.centerx =vichopls.rect.centerx
        self.rect.centery =vichopls.rect.centery
        self.dir = dir
        self.mov = True
    def mover(self):
        if len(self.dir)==1:
            if "u" in self.dir:
                if abs(abs(self.rect.centery - 5) - abs(self.y0)) <200:
                    self.rect.centery-=5
                else:
                    self.kill()
                    self.mov = False
            if "d" in self.dir:
                if abs(abs(self.rect.centery + 5) - abs(self.y0)) <200:
                    self.rect.centery+=5
                else:
                    self.kill()
                    self.mov = False
            if "r" in self.dir:
                if abs(abs(self.rect.centerx + 5) - abs(self.x0)) <200:
                    self.rect.centerx+=5
                else:
                    self.kill()
                    self.mov = False
            if "l" in self.dir:
                if abs(abs(self.rect.centerx - 5) - abs(self.x0)) <200:
                    self.rect.centerx-=5
                else:
                    self.kill()
                    self.mov = False
        if len(self.dir)>1:
            if "u" in self.dir and "r" in self.dir:
                if abs(abs(self.rect.centery - 5) - abs(self.y0)) <200:
                    self.rect.centery-=5
                else:
                    self.kill()
                    self.mov = False
                if abs(abs(self.rect.centerx + 5) - abs(self.x0)) <200:
                    self.rect.centerx+=5
                else:
                    self.kill()
                    self.mov = False
            if "u" in self.dir and "l" in self.dir:
                if abs(abs(self.rect.centery - 5) - abs(self.y0)) <200:
                    self.rect.centery-=5
                else:
                    self.kill()
                    self.mov = False
                if abs(abs(self.rect.centerx - 5) - abs(self.x0)) <200:
                    self.rect.centerx-=5
                else:
                    self.kill()
                    self.mov = False
            if "d" in self.dir and "r" in self.dir:
                if abs(abs(self.rect.centery + 5) - abs(self.y0)) <200:
                    self.rect.centery+=5
                else:
                    self.kill()
                    self.mov = False
                if abs(abs(self.rect.centerx + 5) - abs(self.x0)) <200:
                    self.rect.centerx+=5
                else:
                    self.kill()
                    self.mov = False
            if "d" in self.dir and "l" in self.dir:
                if abs(abs(self.rect.centery + 5) - abs(self.y0)) <200:
                    self.rect.centery+=5
                else:
                    self.kill()
                    self.mov = False
                if abs(abs(self.rect.centerx - 5) - abs(self.x0)) <200:
                    self.rect.centerx-=5
                else:
                    self.kill()
                    self.mov = False
        
        
        
        


class Vicho(pygame.sprite.Sprite):

    def __init__(self, x,imag):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(imag, IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = SCREEN_HEIGHT / 2

    def humano(self):
        # Controlar que la paleta no salga de la pantalla
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH




def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("VichoPLS")

    # cargamos los objetos
    fondo = load_image("fondo.jpg", IMG_DIR, alpha=False)
    jugador1 = Vicho(40,"plox.gif")
    #jugador2 = Vicho(SCREEN_WIDTH-40,"cc.bmp")
    #En esta linea hacemos hacer aparecer al jugador de colo colo que aun no tiene implementada alguna IA
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)
    contadorBalas = 0
    balas = []
    ultimo="r"
    
    # el bucle principal del juego
    try:
        
        while True:
            directores = []
            clock.tick(60)

            # Actualizamos los obejos en pantalla
            jugador1.humano()

            # El input del teclado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            if pygame.key.get_pressed()[K_UP]:
                jugador1.rect.y -= 3
                if not("u" in directores):
                    directores.append("u")
                ultimo = "u"
            if pygame.key.get_pressed()[K_DOWN]:
                jugador1.rect.y += 3
                if not("d" in directores):
                    directores.append("d")
                ultimo = "d"
            if pygame.key.get_pressed()[K_LEFT]:
                jugador1.rect.x -= 3
                if not("l" in directores):
                    directores.append("l")
                ultimo = "l"
            if pygame.key.get_pressed()[K_RIGHT]:
                jugador1.rect.x += 3
                if not("r" in directores):
                    directores.append("r")
                ultimo = "r"
            if pygame.key.get_pressed()[K_k] and contadorBalas == 0:
                d = list(ultimo)
                contadorBalas +=1
                if len(directores)>0 and not("l" in directores and "r" in directores) and not("u" in directores and "d" in directores):
                    balas.append(Bala(jugador1,"bola.png",directores))
                else:
                    balas.append(Bala(jugador1,"bola.png",d))
            if contadorBalas>=1:
                contadorBalas+=1
            if contadorBalas>=20:
                contadorBalas=0
                
        
            # actualizamos la pantalla
            screen.blit(fondo, (0, 0))
            screen.blit(jugador1.image, jugador1.rect)
            if len(balas)>0:
                for i in range(len(balas)):
                    balas[i].mover()
                    if balas[i].mov:
                        screen.blit(balas[i].image,balas[i].rect)
            if len(balas)>0:
                count = 0
                while count<len(balas):
                    if balas[0].mov == False:
                        del balas[0]
                    else:
                        count+=1

            #screen.blit(jugador2.image, jugador2.rect)
            #para hacer aparecer al jugador
            pygame.display.flip()

    except ValueError:
        pass


if __name__ == "__main__":
    main()
