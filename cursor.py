import pygame
from constants import *
from game_objects import *

class Cursor(GameObject):
    
    def __init__(self, position):
        super().__init__([position, CDIM[:]])
        self.color = YELLOW
        self.solid = False

    def paint_self(self, screen, viewport):
        [[x,y],[w,h]] = get_viewport_bounds(self.bounds, viewport)
        pygame.draw.rect(screen, self.color, [x-1, y-1, w+2, h+2], 1)
