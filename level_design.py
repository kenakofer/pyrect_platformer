#!/usr/bin/python3

import pygame
from game_objects import *
from constants import *
from cursor import Cursor
from grid import Grid
from point_track import PointTrack
from limit_guides import LimitGuides

def main():

    # initialize game engine
    pygame.init()

    # set screen width/height and caption
    screen = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption('Level Design')
    # initialize clock. used later in the loop.
    clock = pygame.time.Clock()

    object_list = []
    cursor = Cursor([0,0])
    object_list.append(Grid())
    object_list.append(LimitGuides())
    viewport = Viewport([[0,0],SCREEN_DIM], None, None, None)
    tool=Wall
    tool_stage = 0
    point_list = []
    point_track = PointTrack(point_list)
     
    # Loop until the user clicks close button
    done = False

    print_level_header()

    MOUSEPOS=[0,0]

    #Tool stages
    UNUSED=0
    CLICK_DRAG=1
    POINTS_SELECT=2
    SPEED_SELECT=3
    

    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEMOTION:
                MOUSEPOS=list(event.pos)
                point = snap_point(get_absolute_coordinates(MOUSEPOS, viewport))
                if tool_stage is CLICK_DRAG:
                    cursor.bounds[DIM] = vec_subtract(point, cursor.bounds[POS])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                point = snap_point(get_absolute_coordinates(MOUSEPOS, viewport))
                if tool_stage is UNUSED:
                    if tool is Player:
                        print("    p = Player("+str(point)+")")
                        print_object_addition("p")
                        object_list.append(Player(point))
                    else: #tool is a draggable-bounds thing
                        tool_stage=CLICK_DRAG
                        cursor.bounds[POS] = point

                elif tool_stage is POINTS_SELECT:
                    point_list.append(point)

            elif event.type == pygame.MOUSEBUTTONUP:
                if tool_stage is CLICK_DRAG:
                    if tool is Wall:
                        object_list.append(Wall(cursor.bounds))
                        print_object_addition("Wall("+str(cursor.bounds)+")")
                        tool_stage=UNUSED
                    else: #tool is a moving entity
                        tool_stage=POINTS_SELECT
        #Tool selection
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            tool = Wall
            tool_stage = 0
        elif keys[pygame.K_x]:
            tool = Player
        elif keys[pygame.K_p]:
            tool = Platform
        elif keys[pygame.K_k]:
            tool = Killer
        elif keys[pygame.K_f]:
            tool = Finish
        elif keys[pygame.K_s]:
            tool = SuperWall
        elif keys[pygame.K_RETURN]:
            if tool_stage is POINTS_SELECT:
                #tool_stage=SPEED_SELECT
                o = tool(cursor.bounds, point_list[:], 0)
                object_list.append(o)
                print_object_addition(o.__class__.__name__+"("+str(cursor.bounds)+","+str(point_list)+", 0)")
                point_list.clear()
                tool_stage=UNUSED

        # clear the screen before drawing
        screen.fill(BACK_COLOR) 
        # write draw code here
        for o in object_list:
            try:
                o.paint_self(screen, viewport)
            except (TypeError):
                print(o)
        if tool_stage is CLICK_DRAG or tool_stage is POINTS_SELECT:
            cursor.paint_self(screen, viewport)
        if tool_stage is POINTS_SELECT:
            point_track.paint_self(screen, viewport)


        # display what’s drawn. this might change.
        pygame.display.update()
        # run at FPS fps
        clock.tick(FPS)
    #The user has exited the application; print footer and get out. 
    print_level_footer()
    # close the window and quit
    pygame.quit()

def snap_point(point):
    [x,y]=point
    return [x-(x%CDIM[W]), y-(y%CDIM[H])]


def print_object_addition(object_string):
    print("    object_list.append("+object_string+")")

def print_level_header():
    print("##AUTOMATICALLY GENERATED HEADER##")
    print("from game_objects import *")
    print("def initialize():")
    print("    object_list=[]")

def print_level_footer():
    print("    ##AUTOMATICALLY GENERATED FOOTER##")
    print("    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p")
    print("    return (viewport, object_list)")



if __name__ == '__main__':
    main()
