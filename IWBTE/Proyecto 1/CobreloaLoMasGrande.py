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

class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    #file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()


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
    def __init__(self,imag,_velocidad, _hp):
        self.fr=1
        self.path=imag
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(imag+"l1.gif", IMG_DIR,alpha=True)
        num = randint(0,1)
        self.rect = Rect(0,0,20,30)
        self.rect.centerx=SCREEN_WIDTH-50
        self.rect.centery=SCREEN_HEIGHT*num
        self.velocidad = _velocidad
        self.hp = _hp
        self.vivo = True

    def volanteOMaleta(self, machucao):
        if self.rect.colliderect(machucao.rect) and machucao.inv == False:
            return True
    def mover(self, objetivo, reloj):
        if objetivo.rect.centerx - self.rect.centerx >= 0:
            self.image = load_image(self.path+"r"+str(self.fr)+".gif",IMG_DIR,alpha=False)
            
            self.rect.centerx += self.velocidad*(reloj/30)
            self.fr+=1
            if self.fr>3:
                self.fr=1
        else:
            self.image = load_image(self.path+"l"+str(self.fr)+".gif",IMG_DIR,alpha=False)
            
            self.rect.centerx -= self.velocidad*(reloj/30)
            self.fr+=1
            if self.fr>3:
                self.fr=1
        if objetivo.rect.centery - self.rect.centery >= 0:
            if objetivo.rect.centery - self.rect.centery >= 10:
                self.image = load_image(self.path+"d"+str(self.fr)+".gif",IMG_DIR,alpha=False)
            self.rect.centery += self.velocidad*(reloj/30)
            self.fr+=1
            if self.fr>3:
                self.fr=1
        else:
            if objetivo.rect.centery - self.rect.centery <= -10:
                self.image = load_image(self.path+"u"+str(self.fr)+".gif",IMG_DIR,alpha=False)
            self.rect.centery -= self.velocidad*(reloj/30)
            self.fr+=1
            if self.fr>3:
                self.fr=1

class vichoLover(enemy):
    pass

class zorron(enemy):
    def atacando(self, objetivo):
        pass

class daGame:
    def __init__(self):
        self.balas=[]
        self.energeticas = []
        self.ultimo = "r"
        self.lovers = []
        self.zorrones = []
        self.timeSpawn = 3
        self.enemies = 0
        self.tiempoActual = 0
        self.spawn = 0
        self.eliminacionLovers = False
        self.eliminacionZorron = False
        self.continuar = True

class energyDrink(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.time = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("Drink.gif", IMG_DIR,alpha=True)
        self.rect = Rect(0,0,8,20)
        self.rect.centerx=x
        self.rect.centery=y

    def africano(self, machucao):
        if self.rect.colliderect(machucao.rect):
            return True


def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("VichoPLS")
    clock = pygame.time.Clock()
    fondo = load_image("intro.png", IMG_DIR, alpha=False)
    
    laBala = load_sound("Bala.wav")

    pygame.mixer.music.load("game.wav")
        
        
    pygame.mixer.music.play(-1)

    while True:
        leReloj = float(clock.tick(42))
        screen.blit(fondo, (0, 0))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.continuar = False

        if pygame.key.get_pressed()[K_k]:
            #laBala.play()
            pygame.mixer.stop()
            break
        pygame.display.flip()

    
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
        pygame.mixer.music.load("leJuego.wav")
        
        
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
                    laBala.play()
                    game.balas.append(Bala(jugador1,"Baqueta/Frames/1.gif",directores))
                else:
                    laBala.play()
                    game.balas.append(Bala(jugador1,"bola.png",d))
                
                
            if jugador1.contadorBalas>=1:
                jugador1.contadorBalas+=leReloj
            if jugador1.contadorBalas>=701:
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
            if game.tiempoActual - game.spawn >= game.timeSpawn and game.enemies<5:
               game.spawn = game.tiempoActual
               numeroRandom = uniform(0,1)
               if numeroRandom <= 0.3:
                   game.lovers.append(vichoLover("Lover/Frames/",3,30))
                   
               else:
                   game.zorrones.append(zorron("Zorron/Frames/",2,50))
                   pass
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

            #Eliminando energéticas
            if len(game.energeticas)>0:
                count = 0
                while count<len(game.energeticas):
                    if game.energeticas[count].time>5000:
                        game.energeticas[count].kill()
                        del game.energeticas[count]
                    else:
                        game.energeticas[count].time+=leReloj
                        count+=1

            if len(game.lovers)>0:
                for i in range(len(game.lovers)):
                    if game.lovers[i].vivo==True:
                        game.lovers[i].mover(jugador1,leReloj)
                        screen.blit(game.lovers[i].image,game.lovers[i].rect)

            if len(game.zorrones)>0:
                for i in range(len(game.zorrones)):
                    if game.zorrones[i].vivo==True:
                        game.zorrones[i].mover(jugador1,leReloj)
                        screen.blit(game.zorrones[i].image,game.zorrones[i].rect)

            #Matando Vicholovers
            if len(game.lovers)>0 and len(game.balas)>0:
                for i in range(len(game.balas)):
                    for j in range(len(game.lovers)):
                        if game.balas[i].tunazo(game.lovers[j]) and game.balas[i].mov==True:
                            game.balas[i].mov = False
                            game.balas[i].kill()
                            game.lovers[j].hp -= 10
                            if game.lovers[j].hp <= 0:
                                algunRandom = uniform(0,1)
                                if algunRandom <= 0.3 and len(game.energeticas)<3:
                                    game.energeticas.append(energyDrink(game.zorrones[j].rect.centerx,game.zorrones[j].rect.centery))
                                game.lovers[j].vivo = False
                                game.lovers[j].kill()
                                game.enemies -= 1
                                game.eliminacionLovers = True
                                jugador1.asesinatos+=1

            #Matando Zorrones
            if len(game.zorrones)>0 and len(game.balas)>0:
                for i in range(len(game.balas)):
                    for j in range(len(game.zorrones)):
                        if game.balas[i].tunazo(game.zorrones[j]) and game.balas[i].mov==True:
                            game.balas[i].mov = False
                            game.balas[i].kill()
                            game.zorrones[j].hp -= 10
                            if game.zorrones[j].hp <= 0:
                                algunRandom = uniform(0,1)
                                if algunRandom <= 0.3 and len(game.energeticas)<3:
                                    game.energeticas.append(energyDrink(game.zorrones[j].rect.centerx,game.zorrones[j].rect.centery))
                                game.zorrones[j].vivo = False
                                game.zorrones[j].kill()
                                game.enemies -= 1
                                game.eliminacionZorron = True
                                jugador1.asesinatos+=1

            #Tomando energetica
            if len(game.energeticas)>0:
                count = 0
                while count < (len(game.energeticas)):
                    if game.energeticas[count].africano(jugador1):
                        jugador1.hp=100
                        game.energeticas[count].kill()
                        del game.energeticas[count]
                    else:
                        count += 1


            
                
            
            for energetica in game.energeticas:
                screen.blit(energetica.image,energetica.rect)

            #Eliminando las sobras
            if len(game.lovers)>0 and game.eliminacionLovers:
                count = 0
                while count<len(game.lovers):
                    if game.lovers[count].vivo == False:
                        del game.lovers[count]
                    else:
                        count+=1
                game.eliminacionLovers = False

            if len(game.zorrones)>0 and game.eliminacionZorron:
                count = 0
                while count<len(game.zorrones):
                    if game.zorrones[count].vivo == False:
                        del game.zorrones[count]
                    else:
                        count+=1
                game.eliminacionZorron = False

            #VicholoversAttack
            if len(game.lovers)>0:
                for i in range(len(game.lovers)):
                    if game.lovers[i].vivo and game.lovers[i].volanteOMaleta(jugador1) and not(jugador1.inv):
                        jugador1.inv = True
                        jugador1.lastHited = game.tiempoActual
                        jugador1.dam(30)
                        if jugador1.hp <= 0:
                            jugador1.vivo=False
            
            #ZorronesPower
            if len(game.zorrones)>0:
                for i in range(len(game.zorrones)):
                    if game.zorrones[i].vivo and game.zorrones[i].volanteOMaleta(jugador1) and not(jugador1.inv):
                        jugador1.inv = True
                        jugador1.lastHited = game.tiempoActual
                        jugador1.dam(10)
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
