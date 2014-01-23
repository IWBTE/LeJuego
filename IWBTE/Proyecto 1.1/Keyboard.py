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
        if not("u" in etapa.directores):
            etapa.directores.append("u")
        etapa.ultimo = "u"
    if pygame.key.get_pressed()[K_DOWN]:
        hero.moverAbajo(reloj)
        hero.actualizarFrame("d")
        if not("d" in etapa.directores):
            etapa.directores.append("d")
        etapa.ultimo = "d"
    if pygame.key.get_pressed()[K_LEFT]:
        hero.moverIzquierda(reloj)
        hero.actualizarFrame("l")
        if not("l" in etapa.directores):
            etapa.directores.append("l")
        etapa.ultimo = "l"
    if pygame.key.get_pressed()[K_RIGHT]:
        hero.moverDerecha(reloj)
        hero.actualizarFrame("r")
        if not("r" in etapa.directores):
            etapa.directores.append("r")
        etapa.ultimo = "r"
    if pygame.key.get_pressed()[K_k] and hero.retrasoBalas == 0:
        d = etapa.ultimo
        hero.retrasoBalas=1
        if len(etapa.directores)>0 and not("l" in etapa.directores and "r" in etapa.directores) and not("u" in etapa.directores and "d" in etapa.directores):
            dire = ""
            for letra in etapa.directores:
                dire = dire+letra
            etapa.laBala.play()
            etapa.balas.append(Bala(hero,dire))
        else:
            etapa.laBala.play()
            etapa.balas.append(Bala(hero,d))