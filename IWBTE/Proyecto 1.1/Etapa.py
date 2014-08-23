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

from Serpiente import Serpiente

from Boss import Montes
from Ataques import balazo

from Arbol import Arbol
from Basura import Basura


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
    def __init__(self,_cargaImagen,_clock,_screen, _maxEnemies, _spawnTime, _probabilidadEnergetica, _enemigosEtapa,_jefe,_nombreJefe, _posx, _posy):
        self.cargaImagen = _cargaImagen
        self.fondo = self.cargaImagen("fondo.png", "imagenes", alpha=False)
        self.clock = _clock
        self.screen = _screen
        self.continuar = True
        self.probabilidadEnergetica = _probabilidadEnergetica


        self.cx = _posx
        self.cy = _posy
        self.especialJefe = dict()
        self.especialJefe["Raul"] = self.packRaul
        
        self.especialJefe["Luis"] = self.packLuis
        
        self.enemies = 0
        self.spawnTime = _spawnTime
        self.maxEnemies = _maxEnemies
        self.lastSpawn = 0
        self.spawned = 0
        self.enemigosEtapa = _enemigosEtapa
        self.px = 0
        self.py = 0

        self.killed = 0
        self.jefe = _jefe
        self.nombreJefe = _nombreJefe

        self.balas = []
        self.proyJefe = []
        self.heart = []
        self.energeticas = []
        self.corazones = []
        
        self.lovers = []
        self.zorrones = []

        self.arboles = []
        self.basureros = []

        self.ataqueActual = balazo

        self.laBala = load_sound("Bala.wav")

    def spawnEnemy(self,tiempo):
        if self.lastSpawn>=self.spawnTime and self.enemies<self.maxEnemies and self.spawned < self.enemigosEtapa:
            num = uniform(0,1)
            if num<=0.7:
                self.zorrones.append(Zorron(self.cargaImagen))
            else:
                self.lovers.append(Lover(self.cargaImagen))    
            self.enemies += 1
            self.spawned += 1
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

    def moverProyRaul(self,tiempo,jugador):
        if len(self.proyJefe)>0:
            for i in range(len(self.proyJefe)):
                self.proyJefe[i].mover(tiempo,jugador)
                self.proyJefe[i].cambiarFrame()
                if self.proyJefe[i].mov:
                    (self.screen).blit(self.proyJefe[i].image,self.proyJefe[i].rect)

    def packRaul(self,tiempo,jugador):
        self.raulPower(jugador)
        self.moverProyRaul(tiempo,jugador)
        self.eliminarProyRaul()
        
    def packLuis(self,tiempo,jugador):
        pass
                        
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

    def chaoJefe(self):
        if not(self.jefe.invencible):
            for i in (self.balas):
                if i.tunazo(self.jefe):
                    self.jefe.hp -= 10

    def enamoramiento(self,jugador):
        if len(self.heart)>0:
            for i in (self.heart):
                if i.flechazo(jugador):
                    jugador.hp-=30

    def raulPower(self,jugador):
        if len(self.proyJefe)>0:
            for i in (self.proyJefe):
                var = i.atRaul(jugador)
                if var>0:
                    jugador.hp-=var
                              

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

    def eliminarProyRaul(self):
        if len(self.proyJefe)>0:
            count = 0
            while count < len(self.proyJefe):
                if self.proyJefe[count].mov == False:
                    del self.proyJefe[count]
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

    def danarConJefe(self,jugador):
        if self.jefe.choque(jugador):
            jugador.hp-=10

    def actualizarHP(self,HP,jugador):
        HP.actualizar(jugador)
        (self.screen).blit(HP.image, HP.rect)

    def continuar(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.continuar = False

    def BossBattle(self,ejecutar):
        if ejecutar:
            seguir = True
            while seguir:
                pass

    def Obstaculos(self):
        count = 0
        while count < 4 :
            self.px = randint(0,538)
            self.py = randint(0,380)
            self.arboles.append(Arbol(self.px,self.py,self.cargaImagen))
            count += 1

        count = 0
        while count < 6 :
            self.px = randint(0,595)
            self.py = randint(0,450)
            self.basureros.append(Basura(self.px,self.py,self.cargaImagen))
            count += 1
        

    def ActualizarObstaculos(self):
        for i in self.arboles:
            (self.screen).blit(i.image, i.rect)

        for i in self.basureros:
            (self.screen).blit(i.image, i.rect)
            
        
                

        

    def ejecutarEtapa(self, cancion):

        pygame.mixer.music.load(cancion+".wav")
        pygame.mixer.music.play(-1)
        Vicho = Personaje(self.cargaImagen,self.cx,self.cy)
        miHP = HP(self.cargaImagen)
        self.Obstaculos()

      
        
        while self.continuar and self.killed<self.enemigosEtapa:
            tiempo = float((self.clock).tick(42))
            (self.screen).blit(self.fondo, (0, 0))
            pygame.event.get()     
            Vicho.directores = []   
            keyboard(Vicho,tiempo,self)

            Vicho.margen()
            (self.screen).blit(Vicho.image, Vicho.rect)

            self.spawnEnemy(tiempo)

            self.ActualizarObstaculos()

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
                return False

        
        while True:
            tiempo = float((self.clock).tick(42))
            (self.screen).blit(self.fondo, (0, 0))
            pygame.event.get()     
            Vicho.directores = []   
            keyboard(Vicho,tiempo,self)

            Vicho.margen()
            (self.screen).blit(Vicho.image, Vicho.rect)

            self.moverBalas(tiempo)

            self.chaoJefe()
            self.eliminarBalas()

            
            self.especialJefe[self.nombreJefe](tiempo,Vicho)


            self.jefe.mover(tiempo)
            self.jefe.atacar(tiempo,Vicho,self)


            self.danarConJefe(Vicho)

            (self.screen).blit(self.jefe.image, self.jefe.rect)


            Vicho.poderDisparar(tiempo)

            self.actualizarHP(miHP,Vicho)

            Vicho.invencibilidad(tiempo)
            pygame.display.flip()

            if Vicho.hp <=0:                
                return False
            if self.jefe.hp <=0:
                self.cx = Vicho.rect.centerx
                self.cy = Vicho.rect.centery
                return True
            


