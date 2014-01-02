import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
from threading import Timer
import time
from math import floor

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
        self.count = 1
        self.image = load_image(imag, IMG_DIR, alpha=True)
        self.rect = Rect(0,0,10,10)
        self.x0 = vichopls.rect.centerx
        self.y0 = vichopls.rect.centery
        self.rect.centerx =vichopls.rect.centerx
        self.rect.centery =vichopls.rect.centery+10
        self.dir = dir
        self.mov = True

    def tunazo(self, baleado):
        if self.rect.colliderect(baleado.rect):
            return True


    def mover(self, reloj):
        self.count+=1
        if self.count>8:
            self.count=1
        self.image = load_image("Baqueta/Frames/"+str(self.count)+".gif", IMG_DIR, alpha=True)
        if len(self.dir)==1:
            if "u" in self.dir:
                if abs(abs(self.rect.centery - 5) - abs(self.y0)) <200:
                    self.rect.centery-=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
            if "d" in self.dir:
                if abs(abs(self.rect.centery + 5) - abs(self.y0)) <200:
                    self.rect.centery+=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
            if "r" in self.dir:
                if abs(abs(self.rect.centerx + 5) - abs(self.x0)) <200:
                    self.rect.centerx+=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
            if "l" in self.dir:
                if abs(abs(self.rect.centerx - 5) - abs(self.x0)) <200:
                    self.rect.centerx-=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
        if len(self.dir)>1:
            if "u" in self.dir and "r" in self.dir:
                if abs(abs(self.rect.centery - 5) - abs(self.y0)) <200:
                    self.rect.centery-=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
                if abs(abs(self.rect.centerx + 5) - abs(self.x0)) <200:
                    self.rect.centerx+=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
            if "u" in self.dir and "l" in self.dir:
                if abs(abs(self.rect.centery - 5) - abs(self.y0)) <200:
                    self.rect.centery-=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
                if abs(abs(self.rect.centerx - 5) - abs(self.x0)) <200:
                    self.rect.centerx-=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
            if "d" in self.dir and "r" in self.dir:
                if abs(abs(self.rect.centery + 5) - abs(self.y0)) <200:
                    self.rect.centery+=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
                if abs(abs(self.rect.centerx + 5) - abs(self.x0)) <200:
                    self.rect.centerx+=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
            if "d" in self.dir and "l" in self.dir:
                if abs(abs(self.rect.centery + 5) - abs(self.y0)) <200:
                    self.rect.centery+=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
                if abs(abs(self.rect.centerx - 5) - abs(self.x0)) <200:
                    self.rect.centerx-=5.5*(reloj/30)
                else:
                    self.kill()
                    self.mov = False
        
class hp(pygame.sprite.Sprite):
    def __init__(self,imag):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(imag, IMG_DIR, alpha = True)
        self.rect = self.image.get_rect()
        self.rect.centerx=85
        self.rect.centery=15
                              
class Vicho(pygame.sprite.Sprite):

    def __init__(self, x,imag):
        pygame.sprite.Sprite.__init__(self)
        self.fr = 1
        self.asesinatos = 0
        self.hp = 100
        self.image = load_image(imag, IMG_DIR, alpha=True)
        self.rect = Rect(0,0,10,15)
        self.rect.centerx = x
        self.rect.centery = (SCREEN_HEIGHT / 2)
        self.contadorBalas = 0
        self.inv = False
        self.lastHited = 0
        self.vivo = True

    def humano(self):
        # Controlar que la paleta no salga de la pantalla
        if self.rect.bottom >= SCREEN_HEIGHT-10:
            self.rect.bottom = SCREEN_HEIGHT-10
        elif self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= SCREEN_WIDTH-10:
            self.rect.right = SCREEN_WIDTH-10

    def dam(self,cantidad):
        self.hp -= cantidad


class enemy(pygame.sprite.Sprite):
    def __init__(self,imag):
        self.fr=1
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(imag, IMG_DIR,alpha=True)
        num = randint(0,1)
        self.rect = Rect(0,0,20,30)
        self.rect.centerx=SCREEN_WIDTH-50
        self.rect.centery=SCREEN_HEIGHT*num
        self.hp = 30
        self.vivo = True

    def volanteOMaleta(self, machucao):
        if self.rect.colliderect(machucao.rect) and machucao.inv == False:
            return True
    def mover(self, objetivo, reloj):
        if objetivo.rect.centerx - self.rect.centerx >= 0:
            self.image = load_image("Lover/Frames/r"+str(self.fr)+".gif",IMG_DIR,alpha=False)
            
            self.rect.centerx += 3.2*(reloj/30)
            self.fr+=1
            if self.fr>3:
                self.fr=1
        else:
            self.image = load_image("Lover/Frames/l"+str(self.fr)+".gif",IMG_DIR,alpha=False)
            
            self.rect.centerx -= 3.2*(reloj/30)
            self.fr+=1
            if self.fr>3:
                self.fr=1
        if objetivo.rect.centery - self.rect.centery >= 0:
            if objetivo.rect.centery - self.rect.centery >= 10:
                self.image = load_image("Lover/Frames/d"+str(self.fr)+".gif",IMG_DIR,alpha=False)
            self.rect.centery += 3.2*(reloj/30)
            self.fr+=1
            if self.fr>3:
                self.fr=1
        else:
            if objetivo.rect.centery - self.rect.centery <= -10:
                self.image = load_image("Lover/Frames/u"+str(self.fr)+".gif",IMG_DIR,alpha=False)
            self.rect.centery -= 3.2*(reloj/30)
            self.fr+=1
            if self.fr>3:
                self.fr=1
#Arreglar este desastre
class vichoLover(enemy):
    pass

class daGame:
    def __init__(self):
        self.balas=[]
        self.ultimo = "r"
        self.lovers = []
        self.enemies = 0
        self.tiempoActual = 0
        self.spawn = 0
        self.eliminacion = False
        self.continuar = True

def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("VichoPLS")

    # cargamos los objetos
    miHP = hp("hp100.png")
    fondo = load_image("fondo.png", IMG_DIR, alpha=False)
    jugador1 = Vicho(40,"Vicho/Frames/r1.gif")
    #jugador2 = Vicho(SCREEN_WIDTH-40,"cc.bmp")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)
    game = daGame()
    
    # el bucle principal del juego
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("game.wav")
        pygame.mixer.music.play(-1)
        while jugador1.vivo and game.continuar:
            game.tiempoActual = time.clock()
            directores = []
            leReloj = float(clock.tick(42))
            
            # Actualizamos los obejos en pantalla
            jugador1.humano()

            # El input del teclado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.continuar = False
            if pygame.key.get_pressed()[K_UP]:
                jugador1.image = load_image("Vicho/Frames/u"+str(jugador1.fr)+".gif",IMG_DIR,alpha=False)
                jugador1.rect.y -= (3*(leReloj/30))
                if not("u" in directores):
                    directores.append("u")
                game.ultimo = "u"
            if pygame.key.get_pressed()[K_DOWN]:
                jugador1.image = load_image("Vicho/Frames/d"+str(jugador1.fr)+".gif",IMG_DIR,alpha=False)
                jugador1.rect.y += (3*(leReloj/30))
                if not("d" in directores):
                    directores.append("d")
                game.ultimo = "d"
            if pygame.key.get_pressed()[K_LEFT]:
                jugador1.image = load_image("Vicho/Frames/l"+str(jugador1.fr)+".gif",IMG_DIR,alpha=False)
                jugador1.rect.x -= (3*(leReloj/30))
                if not("l" in directores):
                    directores.append("l")
                game.ultimo = "l"
            if pygame.key.get_pressed()[K_RIGHT]:
                jugador1.image = load_image("Vicho/Frames/r"+str(jugador1.fr)+".gif",IMG_DIR,alpha=False)
                jugador1.rect.x += (3*(leReloj/30))
                if not("r" in directores):
                    directores.append("r")
                game.ultimo = "r"
            if pygame.key.get_pressed()[K_k] and jugador1.contadorBalas == 0:
                d = list(game.ultimo)
                jugador1.contadorBalas +=1
                if len(directores)>0 and not("l" in directores and "r" in directores) and not("u" in directores and "d" in directores):
                    game.balas.append(Bala(jugador1,"Baqueta/Frames/1.gif",directores))
                else:
                    game.balas.append(Bala(jugador1,"bola.png",d))
            if jugador1.contadorBalas>=1:
                jugador1.contadorBalas+=1
            if jugador1.contadorBalas>=20:
                jugador1.contadorBalas=0
                
            jugador1.fr+=1
            if jugador1.fr>3:
                jugador1.fr = 1
            #numero = uniform(0,1)
            #game.enemies += 1
            game.tiempoActual = time.clock()

            if game.tiempoActual - jugador1.lastHited >= 2:
                jugador1.inv = False
            
            #An enemy has been spawned
            if game.tiempoActual - game.spawn >= 3 and game.enemies<10:
               game.spawn = game.tiempoActual
               game.lovers.append(vichoLover("Lover/Frames/l1.gif"))
               game.enemies += 1
        
            # actualizamos la pantalla
            screen.blit(fondo, (0, 0))
            screen.blit(jugador1.image, jugador1.rect)
            
            
            
            

            if len(game.balas)>0:
                for i in range(len(game.balas)):
                    game.balas[i].mover(leReloj)
                    if game.balas[i].mov:
                        screen.blit(game.balas[i].image,game.balas[i].rect)

            #Eliminando balas perdidas
            if len(game.balas)>0:
                count = 0
                while count<len(game.balas):
                    if game.balas[count].mov == False:
                        del game.balas[count]
                    else:
                        count+=1

            if len(game.lovers)>0:
                for i in range(len(game.lovers)):
                    if game.lovers[i].vivo==True:
                        game.lovers[i].mover(jugador1,leReloj)
                        screen.blit(game.lovers[i].image,game.lovers[i].rect)

            #Matando Vicholovers
            if len(game.lovers)>0 and len(game.balas)>0:
                for i in range(len(game.balas)):
                    for j in range(len(game.lovers)):
                        if game.balas[i].tunazo(game.lovers[j]) and game.balas[i].mov==True:
                            game.balas[i].mov = False
                            game.balas[i].kill()
                            game.lovers[j].hp -= 10
                            if game.lovers[j].hp <= 0:
                                game.lovers[j].vivo = False
                                game.lovers[j].kill()
                                game.enemies -= 1
                                game.eliminacion = True
                                jugador1.asesinatos+=1

            #Eliminando las sobras
            if len(game.lovers)>0 and game.eliminacion:
                count = 0
                while count<len(game.lovers):
                    if game.lovers[count].vivo == False:
                        del game.lovers[count]
                    else:
                        count+=1
                game.eliminacion = False

            #VicholoversAttack
            if len(game.lovers)>0:
                for i in range(len(game.lovers)):
                    if game.lovers[i].vivo and game.lovers[i].volanteOMaleta(jugador1) and not(jugador1.inv):
                        jugador1.inv = True
                        jugador1.lastHited = game.tiempoActual
                        jugador1.dam(30)
                        if jugador1.hp <= 0:
                            jugador1.vivo=False

            #screen.blit(jugador2.image, jugador2.rect)
            #para hacer aparecer al jugador
            daHP = int(floor(jugador1.hp))
            if daHP<0:
                daHP=0
            if daHP>100:
                daHP=100
            daHP2 = "hp"+str(daHP)+".png"
            miHP.image = load_image(daHP2,IMG_DIR,alpha=True)
            screen.blit(miHP.image,miHP.rect)

            pygame.display.flip()

    except ValueError:
        pass
    pygame.mixer.quit()
    print "GG"


if __name__ == "__main__":
    main()
