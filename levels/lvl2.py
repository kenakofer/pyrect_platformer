##AUTOMATICALLY GENERATED HEADER##
from game_objects import *
def initialize():
    object_list=[]
    object_list.append(Wall([[176.0, 208.0], [272.0, 80.0]]))
    object_list.append(Wall([[528.0, 128.0], [80.0, 240.0]]))
    object_list.append(Wall([[80.0, 48.0], [48.0, 208.0]]))
    object_list.append(Platform([[176.0, 48.0], [144.0, 32.0]],[[512.0, 48.0], [416.0, 112.0], [384.0, 48.0], [144.0, 304.0], [448.0, 368.0], [128.0, 80.0]], 1))
    p = Player([544.0, 96.0])
    object_list.append(p)
    ##AUTOMATICALLY GENERATED FOOTER##
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)
    return (viewport, object_list)
