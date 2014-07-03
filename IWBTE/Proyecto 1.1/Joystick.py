import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor
from Bala import Bala

def keyboard(hero,reloj,etapa):
    """Controla el input del teclado"""

    pygame.init()
    joysticks = []
    for i in range(0, pygame.joystick.get_count()):
                joysticks.append(pygame.joystick.Joystick(i))
                joysticks[-1].init()
    
    for event in pygame.event.get():
        if event.type == JOYAXISMOTION:
            print "Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion."
            if event.axis == 1 and event.value > 0:
                hero.moverAbajo(reloj)
                hero.actualizarFrame("d")
                if not("d" in hero.directores):
                    hero.directores.append("d")
                hero.ultimo = "d"
            if event.axis == 1 and event.value < 0:
                hero.moverArriba(reloj)
                hero.actualizarFrame("u")
                if not("u" in hero.directores):
                    hero.directores.append("u")
                hero.ultimo = "u" 
            if event.axis == 0 and event.value > 0:
                hero.moverDerecha(reloj)
                hero.actualizarFrame("r")
                if not("r" in hero.directores):
                    hero.directores.append("r")
                hero.ultimo = "r"
            if event.axis == 0 and event.value < 0:
                hero.moverIzquierda(reloj)
                hero.actualizarFrame("l")
                if not("l" in hero.directores):
                    hero.directores.append("l")
                hero.ultimo = "l"
        if event.type == JOYBUTTONDOWN and hero.retrasoBalas == 0:
            etapa.ataqueActual(hero,reloj,etapa)
                
                
                
  
