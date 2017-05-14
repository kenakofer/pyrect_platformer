import pygame
from constants import *
from game_objects import *

class PointTrack(GameObject):
    
    def __init__(self, point_list):
        #super().__init__([, [0,0])
        self.color = RED
        self.solid = False
        self.point_list = point_list

    def paint_self(self, screen, viewport):
        if len(self.point_list) > 1:
            vpoints = [get_viewport_coordinates(p, viewport) for p in self.point_list]
            pygame.draw.lines(screen, self.color, False, vpoints)
        elif len(self.point_list)==1:
            [x,y] = get_viewport_coordinates(self.point_list[0], viewport)
            pygame.draw.line(screen, self.color, [x,y-4], [x,y+4])
            pygame.draw.line(screen, self.color, [x-4,y], [x+4,y])
