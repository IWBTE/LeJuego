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
from Enemy import Lover
from Corazon import Corazon
from HP import HP
from EnergyDrink import EnergyDrink
from Keyboard import keyboard


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
    def __init__(self,_cargaImagen,_clock,_screen, _maxEnemies, _spawnTime, _probabilidadEnergetica):
        self.cargaImagen = _cargaImagen
        self.fondo = self.cargaImagen("fondo.png", "imagenes", alpha=False)
        self.clock = _clock
        self.screen = _screen
        self.continuar = True
        self.probabilidadEnergetica = _probabilidadEnergetica
        
        self.enemies = 0
        self.spawnTime = _spawnTime
        self.maxEnemies = _maxEnemies
        self.lastSpawn = 0

        self.killed = 0

        self.balas = []
        self.heart = []
        self.energeticas = []
        self.corazones = []
        
        self.lovers = []
        self.zorrones = []

        self.laBala = load_sound("Bala.wav")

    def spawnEnemy(self,tiempo):
        if self.lastSpawn>=self.spawnTime and self.enemies<self.maxEnemies:
            num = uniform(0,1)
            if num<=0.7:
                self.zorrones.append(Zorron(self.cargaImagen))
            else:
                self.lovers.append(Lover(self.cargaImagen))    
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

    def moverCorazones(self,leReloj,jugador):
        if len(self.heart)>0:
            for i in range(len(self.heart)):
                self.heart[i].mover(leReloj,jugador)
                self.heart[i].cambiarFrame()
                if self.heart[i].mov:
                    (self.screen).blit(self.heart[i].image,self.heart[i].rect) 
                    
    def moverZorrones(self,leReloj,jugador):
        if len(self.zorrones)>0:
            for i in range(len(self.zorrones)):
                self.zorrones[i].mover(jugador,leReloj,self)
                self.zorrones[i].cambiarFrame()
                if self.zorrones[i].vivo:                
                    (self.screen).blit(self.zorrones[i].image,self.zorrones[i].rect)

    def moverLovers(self,leReloj,jugador):
        if len(self.lovers)>0:
            for i in range(len(self.lovers)):
                self.lovers[i].enamorar(jugador,leReloj,self)
                self.lovers[i].cambiarFrame()
                if self.lovers[i].vivo:
                    (self.screen).blit(self.lovers[i].image,self.lovers[i].rect)
    
    def balacera(self):
        for i in (self.balas):
            if len(self.zorrones)>0:
                for j in range(len(self.zorrones)):
                    if i.tunazo(self.zorrones[j]):
                        self.zorrones[j].hp -= 10
        
            if len(self.lovers)>0:
                for k in range(len(self.lovers)):
                    if i.tunazo(self.lovers[k]):
                        self.lovers[k].hp -= 10

    def enamoramiento(self,jugador):
        if len(self.heart)>0:
            for i in (self.heart):
                if i.flechazo(jugador):
                    jugador.hp-=30
                              

    def eliminarBalas(self):
        if len(self.balas)>0:
            count = 0
            while count<len(self.balas):
                if self.balas[count].mov == False:
                    del self.balas[count]
                else:
                    count+=1

    def eliminarCorazones(self):
        if len(self.heart)>0:
            count = 0
            while count < len(self.heart):
                if self.heart[count].mov == False:
                    del self.heart[count]
                else:
                    count +=1

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
                    self.killed += 1
                else:
                    count+=1

    def eliminarLovers(self):
        if len(self.lovers)>0:
            count = 0
            while count < len(self.lovers):
                if self.lovers[count].hp<=0:
                    self.lovers[count].vivo = False
                    posx = self.lovers[count].rect.centerx
                    posy = self.lovers[count].rect.centery
                    self.spawnearEnergetica(posx,posy)
                    self.lovers[count].kill()
                    del self.lovers[count]
                    self.enemies-=1
                    self.killed += 1
                else:
                    count+=1
    
    def spawnearEnergetica(self, posx, posy):
        a = uniform(0,1)
        if a <= self.probabilidadEnergetica:
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

        if len(self.lovers)>0:
            for i in self.lovers:
                if i.colisionConPersonaje(jugador):
                    jugador.hp-=10

    def actualizarHP(self,HP,jugador):
        HP.actualizar(jugador)
        (self.screen).blit(HP.image, HP.rect)

    def continuar(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.continuar = False

    def ejecutarEtapa(self, cancion):

        pygame.mixer.music.load(cancion+".wav")
        pygame.mixer.music.play(-1)
        Vicho = Personaje(self.cargaImagen)
        miHP = HP(self.cargaImagen) 
        
        while self.continuar and self.killed<=25:
            tiempo = float((self.clock).tick(42))
            (self.screen).blit(self.fondo, (0, 0))
            pygame.event.get()     
            Vicho.directores = []   
            keyboard(Vicho,tiempo,self)

            Vicho.margen()
            (self.screen).blit(Vicho.image, Vicho.rect)

            self.spawnEnemy(tiempo)

            self.moverZorrones(tiempo,Vicho)
            self.moverLovers(tiempo,Vicho)

            self.moverBalas(tiempo)
            self.moverCorazones(tiempo,Vicho)            
            
            self.balacera()
            self.enamoramiento(Vicho)
            self.eliminarZorrones()
            self.eliminarLovers()

            self.energyPack(Vicho,tiempo)

            self.danarPersonaje(Vicho)

            self.eliminarBalas()
            self.eliminarCorazones()

            Vicho.poderDisparar(tiempo)

            self.actualizarHP(miHP,Vicho)

            Vicho.invencibilidad(tiempo)

            pygame.display.flip()

            if Vicho.hp <=0:
                break

            


