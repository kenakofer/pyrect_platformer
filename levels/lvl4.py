##AUTOMATICALLY GENERATED HEADER##
#TODO finish, and fix negatives in coordinates in level_design

from game_objects import *
def initialize():
    object_list=[]
    object_list.append(Wall([[16.0, 16.0], [540.0, 128.0]]))
    #object_list.append(Wall([[512.0, 16.0], [208.0, 32.0]]))
    object_list.append(Wall([[656.0, 16.0], [32.0, 460.0]]))
    object_list.append(Wall([[16.0, 480.0], [672.0, 32.0]]))
    object_list.append(Wall([[16.0, 112.0], [32.0, 400.0]]))
    object_list.append(Wall([[192.0, 192.0], [480.0, 32.0]]))
    object_list.append(Wall([[592.0, 272.0], [32.0, 80.0]]))
    object_list.append(Wall([[496.0, 272.0], [32.0, 80.0]]))
    object_list.append(Wall([[400.0, 272.0], [32.0, 80.0]]))
    object_list.append(Wall([[304.0, 272.0], [32.0, 80.0]]))
    object_list.append(Wall([[208.0, 272.0], [32.0, 80.0]]))
    object_list.append(Wall([[300.0, -150.0], [262.0, 32.0]]))
    object_list.append(Finish([[300.0, -130.0], [32.0, 32.0]], [[]], 0))

    p = Player([580.0, 100.0])
    object_list.append(p)

    object_list.append(Button([[48,474],[32,10]],100,p,lambda x:rotate_objects_around_point(object_list, x.center(),CCW),None))


    ##AUTOMATICALLY GENERATED FOOTER##
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)
    return (viewport, object_list)
