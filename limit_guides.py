import pygame
from constants import *
from game_objects import *

class LimitGuides(GameObject):
    
    def __init__(self):
        #super().__init__([, [0,0])
        self.color = WHITE
        self.solid = False
        self.vertical_values={                  \
                "JUMP_HEIGHT":JUMP_HEIGHT   \
                ,"SUPER_WALL_JUMP_HEIGHT":SUPER_WALL_JUMP_HEIGHT  \
                }
        self.horizontal_values={"JUMP_DISTANCE":JUMP_DISTANCE}


    def paint_self(self, screen, viewport):
        x=0
        for key in self.vertical_values:
            x+=20
            value = self.vertical_values[key]
            onscreen_height = value/viewport.bounds[DIM][H] * SCREEN_DIM[H]
            pygame.draw.line(screen, self.color, [x,SCREEN_DIM[H]-20], [x,SCREEN_DIM[H]-20-onscreen_height])
        y=SCREEN_DIM[H]
        x+=20
        for key in self.horizontal_values:
            y-=20
            value = self.horizontal_values[key]
            onscreen_width = value/viewport.bounds[DIM][W] * SCREEN_DIM[W]
            pygame.draw.line(screen, self.color, [x,y], [x+onscreen_width, y])
