#!/usr/bin/env python3
import pygame
from constants import *
from game_objects import *
import level
import importlib
from copy import deepcopy
import os

#print(os.path.dirname(os.path.abspath(__file__)))

def main():

    # initialize game engine
    pygame.init()
    
    # set screen width/height and caption
    screen = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption('Written by Kenan Bitikofer')

    # initialize clock. used later in the loop.
    clock = pygame.time.Clock()


    #Automatically import all modules within the levels directory.
    #These levels are required to 
    level_modules={}
    for f in os.listdir("./levels"):
        if f.endswith(".py"):
            level_modules[f[:-3]]=(importlib.import_module('levels.'+f[:-3]))
    #print("modules:",level_modules)

    '''
    This list stores a tuple with the initializing function, and the arguments to apply.
    that way, the function can be rerun each time (like if the user fails at a randomly
    generated level, the level will be regenerated new each time).
    '''

    level_initializers = []
    #level_initializers.append((level.physical_limitations_test, ()))
    #level_initializers.append((level_modules['lvl0'].initialize, ()))
    level_initializers.append((level.stuck_in_a_square, (200,500,1,20)))
    level_initializers.append((level_modules['lvl1'].initialize, ()))
    level_initializers.append((level.bounce_wall_climb, (500, 90)))
    level_initializers.append((level_modules['lvl3'].initialize, ()))
    level_initializers.append((level_modules['lvl4'].initialize, ()))
    level_initializers.append((level_modules['button_fun'].initialize, ()))
    level_initializers.append((level.climb_from_death, (500, 1000, .5, 25)))
    current_level_index = 0

    while True:
        #Initialize the level if there are any more
        if current_level_index < len(level_initializers):
            #print("playing level",current_level_index)
            viewport, object_list = level_initializers[current_level_index][0] (*level_initializers[current_level_index][1])
        else:
            print("You beat all the levels!")
            break
        #Run the game loop, ending for appropriate exceptions
        try:
            game_loop(clock, screen, viewport, object_list)
        except (VictoryException):
            current_level_index+=1
        except (FailureException):
            pass
        else:
            #The close button was pressed
            break
     
    # close the window and quit
    pygame.quit()

def game_loop(clock, screen, viewport, object_list):
    # Loop until the user clicks close button.
    done = False
    while done == False:
        # write event handlers here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        #Get input TODO is this efficient?
        keys.clear()
        keys.extend(pygame.key.get_pressed())

        # write game logic here
        for o in object_list:
            o.do_step(object_list)
        #viewport.do_step(object_list)

        # clear the screen before drawing
        screen.fill(BACK_COLOR) 
        # write draw code here
        for o in object_list:
            o.paint_self(screen, viewport)

        #R restarts the level
        if keys[K_R]:
            raise FailureException("Restarting is for losers like you!")



        # display what’s drawn. this might change.
        #pygame.display.update()
        pygame.display.flip()
        # run at FPS fps
        clock.tick(FPS)

if __name__ == '__main__':
    main()

