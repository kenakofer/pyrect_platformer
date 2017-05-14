import pygame
from numpy import arange
from constants import *
from game_objects import *

class Grid(GameObject):
    
    def __init__(self):
        super().__init__([[0,0], SCREEN_DIM[:]])
        self.color = (40,40,40)
        self.solid = False

    def paint_self(self, screen, viewport):
        [[gx,gy],[gw,gh]]=self.bounds
        [[vx,vy],[vw,vh]]=viewport.bounds
        wscale = gw/vw
        hscale = gh/vh
        for i in arange(vx%CDIM[W], SCREEN_DIM[W], CDIM[W]/wscale):
            pygame.draw.lines(screen, self.color, False, [(i,0),(i, SCREEN_DIM[H])], 1)
        for i in arange(vy%CDIM[H], SCREEN_DIM[H], CDIM[H]/hscale):
            pygame.draw.lines(screen, self.color, False, [(0, i), (SCREEN_DIM[W], i)], 1)
