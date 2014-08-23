import pygame
from pygame.locals import *
import os
import sys
from random import uniform
from random import randint
import time
from math import floor

class GameOver:
    def __init__(self,cargaImagen,_clock,_screen):
        self.fondo = cargaImagen("GO.jpg", "imagenes", alpha=False)
        self.clock = _clock
        self.screen = _screen

    def ejecutarMenu(self):
        pygame.mixer.music.load("leDeath.wav")
        pygame.mixer.music.play(-1)
        while True:
            (self.clock).tick(42)
            (self.screen).blit(self.fondo, (0, 0))
            pygame.event.get()
            if pygame.key.get_pressed()[K_w]:
                pygame.mixer.stop()
                return True
            if pygame.key.get_pressed()[K_q]:
                pygame.mixer.stop()
                return False
            pygame.display.flip()
