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
    if pygame.key.get_pressed()[K_UP]:
        hero.moverArriba(reloj)
        hero.actualizarFrame("u")
        if not("u" in hero.directores):
            hero.directores.append("u")
        hero.ultimo = "u"
    if pygame.key.get_pressed()[K_DOWN]:
        hero.moverAbajo(reloj)
        hero.actualizarFrame("d")
        if not("d" in hero.directores):
            hero.directores.append("d")
        hero.ultimo = "d"
    if pygame.key.get_pressed()[K_LEFT]:
        hero.moverIzquierda(reloj)
        hero.actualizarFrame("l")
        if not("l" in hero.directores):
            hero.directores.append("l")
        hero.ultimo = "l"
    if pygame.key.get_pressed()[K_RIGHT]:
        hero.moverDerecha(reloj)
        hero.actualizarFrame("r")
        if not("r" in hero.directores):
            hero.directores.append("r")
        hero.ultimo = "r"
    if pygame.key.get_pressed()[K_k] and hero.retrasoBalas == 0:
        d = hero.ultimo
        hero.retrasoBalas=1
        if len(hero.directores)>0 and not("l" in hero.directores and "r" in hero.directores) and not("u" in hero.directores and "d" in hero.directores):
            dire = ""
            for letra in hero.directores:
                dire = dire+letra
            etapa.laBala.play()
            etapa.balas.append(Bala(hero,dire))
        else:
            etapa.laBala.play()
            etapa.balas.append(Bala(hero,d))