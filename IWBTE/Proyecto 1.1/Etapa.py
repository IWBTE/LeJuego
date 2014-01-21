import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

from Personaje import Personaje

from Bala import Bala
from Enemy import Zorron
from HP import HP
from EnergyDrink import EnergyDrink


class dummysound:
    def play(self): pass

def load_sound(file):
    """Funcion que retorna un sonido"""
    if not pygame.mixer: return dummysound()
    #file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

class Etapa:
    def __init__(self,_cargaImagen,_clock,_screen):
        self.cargaImagen = _cargaImagen
        self.fondo = self.cargaImagen("fondo.png", "imagenes", alpha=False)
        self.clock = _clock
        self.screen = _screen
        self.ultimo = ""
        self.directores = []
        self.enemies = 0
        self.spawnTime = 3000
        self.lastSpawn = 0

        self.balas = []
        self.energeticas = []
        self.corazones = []
        
        self.lovers = []
        self.zorrones = []

        self.laBala = load_sound("Bala.wav")

    def keyboard(self,hero,reloj):
        """Controla el input del teclado"""  
        if pygame.key.get_pressed()[K_UP]:
            hero.moverArriba(reloj)
            hero.actualizarFrame("u")
            if not("u" in self.directores):
                self.directores.append("u")
            self.ultimo = "u"
        if pygame.key.get_pressed()[K_DOWN]:
            hero.moverAbajo(reloj)
            hero.actualizarFrame("d")
            if not("d" in self.directores):
                self.directores.append("d")
            self.ultimo = "d"
        if pygame.key.get_pressed()[K_LEFT]:
            hero.moverIzquierda(reloj)
            hero.actualizarFrame("l")
            if not("l" in self.directores):
                self.directores.append("l")
            self.ultimo = "l"
        if pygame.key.get_pressed()[K_RIGHT]:
            hero.moverDerecha(reloj)
            hero.actualizarFrame("r")
            if not("r" in self.directores):
                self.directores.append("r")
            self.ultimo = "r"
        if pygame.key.get_pressed()[K_k] and hero.retrasoBalas == 0:
            print self.directores
            d = self.ultimo
            hero.retrasoBalas=1
            if len(self.directores)>0 and not("l" in self.directores and "r" in self.directores) and not("u" in self.directores and "d" in self.directores):
                dire = ""
                for letra in self.directores:
                    dire = dire+letra
                self.laBala.play()
                self.balas.append(Bala(hero,dire))
            else:
                self.laBala.play()
                self.balas.append(Bala(hero,d))


    def spawnEnemy(self,tiempo):
        if self.lastSpawn>=self.spawnTime and self.enemies<6:
            self.zorrones.append(Zorron(self.cargaImagen))
            self.enemies += 1
            self.lastSpawn = 0
        else:
            self.lastSpawn+=tiempo

    def moverBalas(self,leReloj):
        if len(self.balas)>0:
            for i in range(len(self.balas)):
                self.balas[i].mover(leReloj)
                self.balas[i].cambiarFrame()
                if self.balas[i].mov:
                    (self.screen).blit(self.balas[i].image,self.balas[i].rect) 
                    
    def moverZorrones(self,leReloj,jugador):
        if len(self.zorrones)>0:
            for i in range(len(self.zorrones)):
                self.zorrones[i].mover(jugador,leReloj,self)
                self.zorrones[i].cambiarFrame()
                if self.zorrones[i].vivo:                
                    (self.screen).blit(self.zorrones[i].image,self.zorrones[i].rect) 
    
    def balacera(self):
        for i in (self.balas):
            if len(self.zorrones)>0:
                for j in range(len(self.zorrones)):
                    if i.tunazo(self.zorrones[j]):
                        self.zorrones[j].hp -= 10
                              

    def eliminarBalas(self):
        if len(self.balas)>0:
            count = 0
            while count<len(self.balas):
                if self.balas[count].mov == False:
                    del self.balas[count]
                else:
                    count+=1

    def eliminarZorrones(self):
        if len(self.zorrones)>0:
            count = 0
            while count < len(self.zorrones):
                if self.zorrones[count].hp<=0:
                    self.zorrones[count].vivo = False
                    posx = self.zorrones[count].rect.centerx
                    posy = self.zorrones[count].rect.centery
                    self.spawnearEnergetica(posx,posy)
                    self.zorrones[count].kill()
                    del self.zorrones[count]
                    self.enemies-=1
                else:
                    count+=1
    
    def spawnearEnergetica(self, posx, posy):
        a = uniform(0,1)
        if a <= 0.7:
            self.energeticas.append(EnergyDrink(posx,posy,self.cargaImagen))

    def tomarEnergetica(self, jugador):
        for i in self.energeticas:
            if i.bebible:
                (self.screen).blit(i.image,i.rect)
                if i.africano(jugador):
                    jugador.hp = 100

    def tiempoEnergeticas(self, tiempo):
        for i in self.energeticas:
            if i.bebible:
                i.tomameODejame(tiempo)

    def eliminarEnergeticas(self):
        if len(self.energeticas)>0:
            count = 0
            while count<(len(self.energeticas)):
                if not(self.energeticas[count].bebible):
                    del self.energeticas[count]
                else:
                    count+=1

    def energyPack(self,jugador,tiempo):
        self.tomarEnergetica(jugador)
        self.tiempoEnergeticas(tiempo)
        self.eliminarEnergeticas()



    def danarPersonaje(self,jugador):
        if len(self.zorrones)>0:
            for i in self.zorrones:
                if i.colisionConPersonaje(jugador):
                    jugador.hp-=10

    def actualizarHP(self,HP,jugador):
        HP.actualizar(jugador)
        (self.screen).blit(HP.image, HP.rect)


    def ejecutarEtapa(self, cancion):

        pygame.mixer.music.load(cancion+".wav")
        pygame.mixer.music.play(-1)
        Vicho = Personaje(self.cargaImagen)
        miHP = HP(self.cargaImagen) 

        while True:
            tiempo = float((self.clock).tick(42))
            (self.screen).blit(self.fondo, (0, 0))
            pygame.event.get() 
            
            self.directores = []          
            self.keyboard(Vicho,tiempo)

            Vicho.margen()
            (self.screen).blit(Vicho.image, Vicho.rect)

            self.spawnEnemy(tiempo)
            self.moverZorrones(tiempo,Vicho)

            self.moverBalas(tiempo)
            self.balacera()
            self.eliminarZorrones()

            self.energyPack(Vicho,tiempo)

            self.danarPersonaje(Vicho)

            self.eliminarBalas()
            Vicho.poderDisparar(tiempo)

            self.actualizarHP(miHP,Vicho)

            Vicho.invencibilidad(tiempo)

            pygame.display.flip()

            if Vicho.hp <=0:
                break

            


