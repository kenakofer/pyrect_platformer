##AUTOMATICALLY GENERATED HEADER##
from game_objects import *
def initialize():
    object_list=[]
    object_list.append(Wall([[48.0, 416.0], [624.0, 32.0]]))
    platform = Platform([[48.0, 464.0], [96.0, 16.0]],[[48,464]], 1.5)
    object_list.append(platform)
    release=lambda b:b.release()
    b1=Button([[64,412],[48,10]],1,platform,lambda p:setattr(p,'move_points',[[48,464]]),None)
    b2=Button([[590,412],[48,10]],1,platform,lambda p:setattr(p,'move_points',[[576,464]]),None)
    b3=Button([[300,412],[48,10]],1,platform,lambda p:setattr(p,'move_points',[[288,80]]),None)
    object_list.append(b1)
    object_list.append(b2)
    object_list.append(b3)
    object_list.append(Killer([[48.0, 258.0], [256.0, 32.0]],[], 0))
    object_list.append(Killer([[368.0, 258.0], [304.0, 32.0]],[], 0))
    object_list.append(Finish([[304.0, 16.0], [32.0, 16.0]],[[304.0, 16.0]], 0))
    p = Player([68,350])
    object_list.append(p)
    ##AUTOMATICALLY GENERATED FOOTER##
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)
    return (viewport, object_list)
