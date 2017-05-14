import pygame
from game_objects import *
from constants import *
from numpy import arange
import random

def level_template():
    object_list = []
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, None)
    object_list.append(viewport)
    return (object_list, viewport)


def stuck_in_a_square(side, distance, speed, clutter_amount):
    object_list = []
    p = Player([50,50])
    object_list.append(p)
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)
    
    width=20
    [x,y]=[0,0]
    object_list.append(Platform([[x,y],[width,side]] \
        ,[[x,y],[x+distance,y],[x+distance,y+distance],[x,y+distance]], speed))
    [x,y]=[0,0]
    object_list.append(Platform([[x,y],[side,width]] \
        ,[[x,y],[x+distance,y],[x+distance,y+distance],[x,y+distance]], speed))
    [x,y]=[side-width,0]
    object_list.append(Platform([[x,y],[width,side]] \
        ,[[x,y],[x+distance,y],[x+distance,y+distance],[x,y+distance]], speed))
    [x,y]=[0,side-width]
    object_list.append(Platform([[x,y],[side,width]] \
        ,[[x,y],[x+distance,y],[x+distance,y+distance],[x,y+distance]], speed))


    for i in range(clutter_amount):
        x=random.randrange(0,side+distance)
        y=random.randrange(0,side+distance)
        w=random.randrange(3,12)**2
        h=random.randrange(3,12)**2
        object_list.append(Wall([[x,y],[w,h]]))

    return (viewport, object_list)

def climb_from_death(width, height, speed, platform_interval):
    object_list = []
    p = Player([-30,height-50])
    object_list.append(p)
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)

    #Base platform
    object_list.append(Wall([[-40,height],[width+40,20]]))
    

    #Platforms to save you!
    for i in range(0,height,platform_interval):
        w=random.randrange(3,6)*16
        h=15
        y=i
        x=random.randrange(0,width-w)
        if random.random()<.1:
            object_list.append(Platform([[x,y],[w,h]],[[0,y],[width-w,y]],1))
        else:
            object_list.append(Wall([[x,y],[w,h]]))


    #Killer chaser
    object_list.append(Killer([[-4000,height+150],[width+8000,5000]], [[-4000,0]], speed))

    #Safety platforms
    object_list.append(Wall([[-60,-20],[60,50]]))
    object_list.append(Wall([[width,-20],[60,50]]))

    #Finish object
    object_list.append(Finish([[-60, -100], [10,10]], [[]], 0))
    object_list.append(Finish([[width+50, -100], [10,10]], [[]], 0))

    return (viewport, object_list)

def bounce_wall_climb(height, interval):
    width=250
    object_list = []
    p = Player([width/2,height-40])
    object_list.append(p)
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)

    #side walls
    object_list.append(Wall([[-30,0],[30,height]]))
    object_list.append(Wall([[width,0],[30,height]]))
    #base
    object_list.append(Wall([[-30,height],[width+60,30]]))

    for i in range(height, 0, -interval):
        gap=65
        object_list.append(Wall([[gap, i],[width-2*gap,6]]))

    object_list.append(Finish([[-4000, height+40], [10000,10000]],[[]], 0))

    return (viewport, object_list)

'''
Reads constants such JUMP_HEIGHT, JUMP_DISTANCE, etc, and constructs a testing
ground to ensure their accuracy.
'''
def physical_limitations_test():
    object_list = []
    p = Player([0,-50])
    object_list.append(p)
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)

    #Floor
    object_list.append(Wall([[-200,0],[700,20]]))
    #Jump height pillar
    object_list.append(Wall([[-150,-JUMP_HEIGHT],[30,50]]))
    #SuperWall jump height pillar and floor
    object_list.append(Wall([[550,-SUPER_WALL_JUMP_HEIGHT],[30,100]]))
    object_list.append(SuperWall([[500,0],[200,20]],[[0,0]],0))
    #Jump distance platforms
    object_list.append(Wall([[30,-40],[60,45]]))
    object_list.append(Wall([[30+60+JUMP_DISTANCE,-40],[60,45]]))
    #Walk speed indicator
    object_list.append(Platform([[-200,20],PLAYER_DIM],[[-200,20],[600,20]],WALK_SPEED))

    return (viewport, object_list)

#TODO Consistency must be achieved in the collision handling for high bounces
def super_wall_height_climbing():
    object_list = []
    p = Player([0,-PLAYER_DIM[H]])
    object_list.append(p)
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)

    #Walls
    object_list.append(Wall([[-200,-500],[20,560]]))
    object_list.append(Wall([[400, -500],[20,560]]))
    
    #Platforms
    interval=JUMP_HEIGHT-10
    #Left
    for i in arange(-SUPER_WALL_JUMP_HEIGHT+10, -1000, -2*interval):
        object_list.append(Wall([[-200,i],[100,20]]))
        print(i)
    #Right
    for i in arange(-SUPER_WALL_JUMP_HEIGHT+10-interval, -1000, -2*interval):
        object_list.append(Wall([[300,i],[100,20]]))
        print(i)

    #Floor
    object_list.append(SuperWall([[-200, 0],[700,30]],[[0,0]],0))

    return (viewport, object_list)

def generated1():
    object_list=[]
    object_list.append(Wall([[32.0, 432.0], [624.0, 32.0]]))
    object_list.append(Wall([[48.0, 32.0], [32.0, 416.0]]))
    object_list.append(Wall([[592.0, 32.0], [48.0, 416.0]]))
    object_list.append(Platform([[48.0, 304.0], [32.0, 128.0]],[[48.0, 304.0], [592.0, 288.0]], 1))
    object_list.append(Killer([[592.0, 272.0], [48.0, 96.0]],[[592.0, 272.0], [48.0, 240.0]], 1))
    p = Player([352.0, 368.0])
    object_list.append(p)
    ##AUTOMATICALLY GENERATED FOOTER##
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)
    return (viewport, object_list)
