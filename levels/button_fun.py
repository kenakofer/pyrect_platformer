##AUTOMATICALLY GENERATED HEADER##
from game_objects import *
from random import randint
def initialize():
    object_list=[]
    #player
    p = Player([400.0, 416.0])
    object_list.append(p)

    def rand_color():
        return (randint(0,2)*127,randint(0,2)*127,randint(0,2)*127)

    b1 = Button([[450, 458],[40,10]],1.1,p,lambda x:setattr(x,'color',rand_color()),None)
    b2 = Button([[350, 458],[40,10]],1.1,p,lambda x:setattr(x,'bounds',[[x.bounds[0][0],x.bounds[0][1]-80],x.bounds[1]]),None)
    b3 = Button([[250, 458],[40,10]],100,p,lambda x:setattr(x,'visible',False),lambda x:setattr(x,'visible',True))
    b4 = Button([[150, 458],[40,10]],300,p,lambda x:rotate_objects_around_point(object_list,x.center(),CW),None)

    object_list.append(b1)
    object_list.append(b2)
    object_list.append(b3)
    object_list.append(b4)

    #floor
    object_list.append(Wall([[48.0, 464.0], [640.0, 32.0]]))

    #Finish
    object_list.append(Finish([[-400,-500],[32,800]], [[]], 0)) 

    ##AUTOMATICALLY GENERATED FOOTER##
    viewport = Viewport([[0,0],[640,480]], Viewport.viewport_differential, Viewport.viewport_differential, p)
    object_list.append(viewport)
    return (viewport, object_list)
