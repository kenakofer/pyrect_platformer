##AUTOMATICALLY GENERATED HEADER##
from game_objects import *
def initialize():
    object_list=[]
    object_list.append(Wall([[48.0, 16.0], [32.0, 480.0]]))
    object_list.append(Wall([[656.0, 16.0], [32.0, 480.0]]))
    object_list.append(Wall([[128.0, 400.0], [96.0, 16.0]]))
    object_list.append(Wall([[256.0, 368.0], [96.0, 16.0]]))
    pl = Platform([[560, 336.0], [96.0, 16.0]],[[384.0, 336.0], [560.0, 336.0]], 0)
    object_list.append(pl)

    b = Button([[450, 458],[50,10]],.1,pl,lambda x:setattr(x,'speed',1),lambda x:setattr(x,'speed',0))
    object_list.append(b)

    #floor
    object_list.append(Wall([[48.0, 464.0], [640.0, 32.0]]))
    object_list.append(Wall([[512.0, 272.0], [32.0, 64.0]]))
    object_list.append(Wall([[512.0, 352.0], [32.0, 128.0]]))
    object_list.append(Finish([[600.0, 404.0], [50, 50]],[[560.0, 336.0]], 0))
    p = Player([400.0, 416.0])
    object_list.append(p)
    ##AUTOMATICALLY GENERATED FOOTER##
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)
    return (viewport, object_list)
