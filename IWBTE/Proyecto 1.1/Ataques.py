import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor
from Bala import Bala

def balazo(hero,reloj,etapa):
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