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
        etapa.ataqueActual(hero,reloj,etapa)
    if pygame.key.get_pressed()[K_ESCAPE]:
        etapa.asd = True