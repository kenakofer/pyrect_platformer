#!/usr/bin/python3

import pygame
from game_objects import *
from constants import *
from cursor import Cursor
from grid import Grid
from point_track import PointTrack
from limit_guides import LimitGuides

tool_tuples = [
        (Wall, 'W', pygame.K_w, "Click and drag"), 
        (Player, 'X', pygame.K_x, "Click"),
        (Platform, 'P', pygame.K_p, "Click and drag"),
        (Killer, 'K', pygame.K_k, "Click and drag"),
        (Finish, 'F', pygame.K_f, "Click and drag"),
        (SuperWall, 'S', pygame.K_s, "Click and drag"),
        ]

def main():

    # initialize game engine
    pygame.init()
    pygame.font.init()

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
    tool_stage = UNUSED
    point_list = []
    point_track = PointTrack(point_list)

    status_message = START_STATUS
     
    # Loop until the user clicks close button
    done = False

    print_level_header()

    mouse_pos=[0,0]


    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos=list(event.pos)
                point = snap_point(get_absolute_coordinates(mouse_pos, viewport))
                if tool_stage is CLICK_DRAG:
                    cursor.bounds[DIM] = vec_subtract(point, cursor.bounds[POS])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                point = snap_point(get_absolute_coordinates(mouse_pos, viewport))
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
                        status_message = POINTS_SELECT_STATUS
        #Tool selection
        keys = pygame.key.get_pressed()
        for t in tool_tuples:
            if keys[t[2]]:
                tool = t[0]
                status_message = t[3] + ' to place a ' + t[0].__name__
                if tool == Wall:
                    tool_stage = 0
                break;
        if keys[pygame.K_RETURN]:
            if tool_stage is POINTS_SELECT:
                #tool_stage=SPEED_SELECT
                o = tool(cursor.bounds, point_list[:], 0)
                object_list.append(o)
                print_object_addition(o.__class__.__name__+"("+str(cursor.bounds)+","+str(point_list)+", 0)")
                point_list.clear()
                tool_stage=UNUSED
                status_message = "You made a "+tool.__name__

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
        paint_menu(screen, tool, status_message)


        # display what’s drawn. this might change.
        pygame.display.update()
        # run at FPS fps
        clock.tick(FPS)
    #The user has exited the application; print footer and get out. 
    print_level_footer()
    # close the window and quit
    pygame.quit()

def paint_menu(screen, active_tool, status_message):
    # First draw the status message
    FONT.set_bold(False)
    FONT.set_italic(True);
    text_surface = FONT.render(status_message, False, STATUS_MESSAGE_COLOR)
    screen.blit(text_surface, (3, 3))
    FONT.set_italic(False);

    x = 3
    y = 30
    for t in tool_tuples:
        FONT.set_bold(False)
        if active_tool == t[0]:
            FONT.set_bold(True);
        # Display the class name
        text_surface = FONT.render(t[0].__name__ + ' ('+t[1]+')', False, TOOL_DISPLAY_COLOR)
        screen.blit(text_surface, (x,y));
        y += TOOL_DISPLAY_HEIGHT


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
