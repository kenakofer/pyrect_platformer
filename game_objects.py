from constants import *
import pygame
from math import copysign

#global. keeps track of which way is down
display_direction=VDOWN

class GameObject:
    
    '''bounds is two points in a list'''
    def __init__(self, bounds):
        self.bounds = bounds[:]
        self.intpos = list(map(int,self.bounds[0]))
        self.dim = bounds[1]
        self.vel = [0,0]
        self.friction=.9
        self.solid = False;
        self.elasticity = WALL_ELASTICITY
        self.color = PINK
        self.visible = True

    def do_step(self, ol):
        self.bounds[0] = vec_add(self.bounds[0], self.vel)
        self.intpos = list(map(int,self.bounds[0]))

    def paint_self(self, screen, viewport):
        if self.visible:
            vbounds=get_viewport_bounds(self.bounds, viewport)
            pygame.draw.rect(screen, self.color, vbounds[0]+vbounds[1], 0)

        
    def shift_bounds(self, vec):
        return [vec_add(self.bounds[0],vec), self.bounds[1]]

    def center(self):
        [[x,y],[w,h]]=self.bounds
        return [x+w/2,y+h/2]

    #TODO actually make sure it's the first one
    def get_first_collider(self, ol):
        shifted = self.shift_bounds(self.vel)
        for o in ol:
            if self is not o \
                    and o.solid \
                    and bounds_overlap(o.shift_bounds(o.vel), shifted):
                return o
        return None


    def on_ground(self, ol):
        for o in ol:
            if self is not o \
               and o.solid \
               and bounds_overlap(o.bounds, shift_bounds_static(self.bounds,[0,1])):
                    return o
        return None

    def left_of(self, ol):
        for o in ol:
            if self is not o \
               and o.solid \
               and bounds_overlap(o.bounds, shift_bounds_static(self.bounds,[1,0])) \
               and not bounds_overlap(o.bounds, self.bounds):
                    return o
        return None

    def right_of(self, ol):
        for o in ol:
            if self is not o \
               and o.solid \
               and bounds_overlap(o.bounds, shift_bounds_static(self.bounds,[-1,0])) \
               and not bounds_overlap(o.bounds, self.bounds):
                    return o
        return None

    '''
    Determines whether an object should be in the computation and drawing
    queue. For example, most object far outside the viewport would be silly to
    continually run steps for or draw off-screen.
    '''
    def is_active(self, ol):
        return True

    '''
    Given two overlapping bodies, returns one of UP, DOWN, LEFT, or RIGHT. At
    this time, the decision is based soley on which direction is the shortest
    to resolve out of the collision
    '''
    def get_collision_direction(self, collider):
        b1=self.bounds
        b2=collider.bounds
        amount={}
        amount[UP]=     abs(b1[POS][Y]-(b2[POS][Y]-b1[DIM][H]))
        amount[DOWN]=   abs(b1[POS][Y]-(b2[POS][Y]+b2[DIM][H]))
        amount[LEFT]=   abs(b1[POS][X]-(b2[POS][X]-b1[DIM][W]))
        amount[RIGHT]=  abs(b1[POS][X]-(b2[POS][X]+b2[DIM][W]))
        minindex = min(amount, key=amount.get)
        return minindex, amount[minindex]

    def rotate_around_point(self, point, direction):
        [[x,y],[w,h]] = self.bounds
        corners=[[x,y],[x+w,y],[x,y+h],[x+w,y+h]]
        if direction is CW:
            corners = [[c2,-c1] for [c1,c2] in corners]
            self.vel = [self.vel[Y],-self.vel[X]]
        elif direction is CCW:
            corners = [[-c2,c1] for [c1,c2] in corners]
            self.vel = [-self.vel[Y],self.vel[X]]
        #Turn corners back into xywh
        minx=1000000000000000
        miny=1000000000000000
        maxx=-100000000000000
        maxy=-100000000000000
        for c in corners:
            if c[X]<minx:
                minx=c[X]
            if c[X]>maxx:
                maxx=c[X]
            if c[Y]<miny:
                miny=c[Y]
            if c[Y]>maxy:
                maxy=c[Y]
        self.bounds=[[minx,miny],[maxx-minx,maxy-miny]]
        #print("New bounds are:",self.bounds)




class Wall(GameObject):
    
    def __init__(self, bounds):
        super().__init__(bounds)
        self.solid=True
        self.color=WALL_COLOR
        self.vel=[0,0]

    def do_step(self, ol):
        self.friction_players(ol)

    def friction_players(self, ol):
        for o in ol:
            if isinstance(o, Player) and not o.frictioned and bounds_overlap(o.bounds, self.shift_bounds([0,-1])):
                o.vel = vec_subtract(o.vel, self.vel)
                o.vel[0]*=o.friction
                o.vel = vec_add(o.vel, self.vel)
                o.frictioned = True #Now no other platform can slow the player this step


class Platform(Wall):
    
    def __init__(self, bounds, points, speed):
        super().__init__(bounds)
        self.color=PLATFORM_COLOR
        self.move_points=points
        self.speed=speed
        self.solid=True
        self.dest=0         #Index of move_points 

    def do_step(self, ol):

        self.move_between_points()

        #resolve collisions with a player object`
        ps = self.get_player_collisions(ol)
        for p in ps:
            p.resolve_collision(self)
            pass

        #Special friction for player
        self.friction_players(ol)
    
    def move_between_points(self):
        if self.speed is 0 or self.move_points==[]:
            self.vel=[0,0]
            return

        diff_vec = vec_subtract(self.move_points[self.dest], self.bounds[0]) 
        dist_to_dest = vec_length(diff_vec)

        if dist_to_dest < self.speed:
            self.vel = diff_vec
            self.dest = (self.dest+1)%len(self.move_points)

        else:
            self.vel = vec_multiple(diff_vec, self.speed/dist_to_dest)

        #velocity enactment
        self.bounds[0] = vec_add(self.bounds[0], self.vel)


    def get_player_collisions(self, ol):
        shifted = self.shift_bounds(self.vel)
        colliders = []
        for o in ol:
            if isinstance(o, Player) \
                    and bounds_overlap(o.shift_bounds(o.vel), shifted):
                colliders.append(o)
        return colliders


class Killer(Platform):

    def __init__(self, bounds, points, speed):
        super().__init__(bounds, points, speed)
        self.solid=False
        self.color=KILLER_COLOR

    def do_step(self, ol):
        self.move_between_points()
        for p in ol:
            if isinstance(p, Player) \
                    and bounds_overlap(p.bounds, self.bounds):
                p.die("I'm a killer wall, and I killed you!");

class Finish(Platform):

    def __init__(self, bounds, points, speed):
        super().__init__(bounds, points, speed)
        self.solid=False
        self.color=FINISH_COLOR

    def do_step(self, ol):
        self.move_between_points()
        for p in ol:
            if isinstance(p, Player) \
                    and bounds_overlap(p.bounds, self.bounds):
                p.win("You won this level!");


class SuperWall(Platform):
    
    def __init__(self, bounds, points, speed):
        super().__init__(bounds, points, speed)
        self.color=SUPER_WALL_COLOR
        self.elasticity=SUPER_WALL_ELASTICITY

class Button(GameObject):

    def __init__(self, bounds, time_down, target, target_function_on, target_function_off):
        super().__init__(bounds)
        self.color=BUTTON_COLOR
        self.solid=False
        self.target = target
        self.target_function_on = target_function_on
        self.target_function_off = target_function_off
        self.time_down = time_down
        self.pressed = False
        self.counter = time_down

    def do_step(self, ol):
        '''
        If the button's pressed,
            If time_down is above zero, decrement it
                if that puts the button at or below zero, run the traget function for off
            Otherwise, this must be a permanent button, so we'll just chill.
        '''
        if self.pressed:
            if self.counter >= 0:
                self.counter-=1
                if self.counter <= 0:
                    self.release()
            else:
                #button is on permanent press
                pass

        '''
        When player is on a button, make sure the counter stays at its max as
        long as she's there.  Only on first contact should the target function
        be run.
        '''
        for p in ol:
            if isinstance(p, Player) \
                    and bounds_overlap(p.bounds, self.bounds):
                self.push()

    '''
    Takes a list of functions or a function and a list of targets or a target,
    and does something intuitive in applying them to each other.
    '''
    def functions_to_targets(f, t):
        if isinstance(f, list):
            if isinstance(t, list):
                if len(f) != len(t):
                    raise Exception("Lists of functions and targets are different lengths")
                else:
                    for i in range(0,len(f)):
                        f[i](t[i])
            else:
                for fi in f:
                    fi(t)
        else:
            if isinstance(t, list):
                for ti in t:
                    f(ti)
            else:
                f(t)

    def push(self):
        self.counter = self.time_down
        if not self.pressed:
            self.pressed = True
            self.visible = False
            if self.target_function_on:
                Button.functions_to_targets(self.target_function_on, self.target)

    def release(self):
        self.counter=0
        self.pressed = False
        self.visible = True
        if self.target_function_off:
            Button.functions_to_targets(self.target_function_off, self.target)


class Dynamic(GameObject):
    
    def __init__(self, bounds, mass):
        super().__init__(bounds)
        self.dynamic = True
        self.mass = True
        self.vel = [0,0]
        self.color = DYNAMIC_COLOR
        self.elasticity = PLAYER_ELASTICITY_CONTROLLED
        self.friction=WALL_FRICTION
        self.ground = None
        self.frictioned = False  #Flag to prevent more than one underfoot platform from each slowing you.


    '''
    Resolves the IMMINENT collision of the player and another object, and
    changes their velocities apropriately. It first normalizes the velocities
    into the frame of reference of collider. It then moves self slowly into the
    collider, so they just overlap by a fraction of their velocities. Then the
    collision direction is determined, and self is moved exactly to the
    appropriate bound of collider. Then new velocity is determined for self.
    Elasticity will determine the primary energy transfer (along the collision
    direction) and friction will determine the lateral energy transfer
    (perpendicular to collision direction). Velocities are then put back in the
    universal frame.
    '''
    def resolve_collision(self, collider):
        #reference frame
        ref_frame=collider.vel[:] #Will bring collider.vel to 0
        self.vel = vec_subtract(self.vel, ref_frame)
        self.save_vspeed = self.vel[Y]
        self.save_pos=self.bounds[POS]
        collider.vel = vec_subtract(collider.vel, ref_frame)
        #Move inside
        if vec_length(self.vel)>.000000001:
            iv = vec_multiple(self.vel, .1)
            #print(iv)
            break_count=0
            while not bounds_overlap(self.bounds, collider.bounds):
                self.bounds=self.shift_bounds(iv)
                break_count+=1
                if break_count>20:
                    self.bounds[POS]=self.save_pos
                    #print("Something happened there with collisions...")
                    break
                    #raise Exception("Whoah, serious issue here with collision resolution!")
        direction, amount=self.get_collision_direction(collider)
        #Resolve out of overlap
        extra=0
        if direction is UP:
            self.bounds[POS][Y] = collider.bounds[POS][Y]-self.bounds[DIM][H] - extra
        if direction is DOWN:
            self.bounds[POS][Y] = collider.bounds[POS][Y]+collider.bounds[DIM][H] + extra
        if direction is LEFT:
            self.bounds[POS][X] = collider.bounds[POS][X]-self.bounds[DIM][W] - extra
        if direction is RIGHT:
            self.bounds[POS][X] = collider.bounds[POS][X]+collider.bounds[DIM][W] + extra

        #Adjust velocities 
        #Decide on player elasticity
        if keys[LSHIFT] or (direction is UP and keys[UP]):
            self.elasticity = PLAYER_ELASTICITY_BOUNCY
        else:
            self.elasticity = PLAYER_ELASTICITY_CONTROLLED

        #TODO take into account impulse effect on collider. Also, refactor this mess
        bounce=self.elasticity*collider.elasticity
        rub=1-(1-self.friction)*(1-collider.friction)
        if direction is UP or direction is DOWN:
            self.vel[Y]= -1 * bounce * self.vel[Y]
            #Limiter to cap the power of super walls
            if abs(self.vel[Y]) > SUPER_WALL_ELASTICITY*JUMP_SPEED:
                self.vel[Y] = copysign(max(SUPER_WALL_ELASTICITY*JUMP_SPEED, abs(self.save_vspeed)), self.vel[Y]);
            #Horizontal friction
            self.vel[X]= rub * self.vel[X]
        if direction is RIGHT or direction is LEFT:
            if isinstance(collider, SuperWall):
                bounce = self.elasticity*SUPER_WALL_HORIZONTAL_ELASTICITY
            self.vel[X]= -1 * bounce * self.vel[X]
            #Cap speed here to the same as a vertical jump on super wall
            if abs(self.vel[X]) > SUPER_WALL_ELASTICITY*JUMP_SPEED:
                self.vel[X] = copysign(SUPER_WALL_ELASTICITY*JUMP_SPEED, self.vel[X]);
            
        #Reverse reference frame
        self.vel = vec_add(self.vel, ref_frame)
        collider.vel = vec_add(collider.vel, ref_frame)
        return amount

    def do_step(self, ol):
        self.frictioned = False
        self.ground = self.on_ground(ol)
        if self.ground:
            if abs(self.vel[1]-self.ground.vel[1]) < GROUNDING_SPEED:
                self.vel[1] = self.ground.vel[1]
        else:
            self.vel = vec_add(self.vel, GRAVITY)
            self.vel = vec_multiple(self.vel, AIR_FRICTION)
            
        ####################
        #collision handling#
        collision_count=0
        c=self.get_first_collider(ol)
        while c is not None:
            c=self.get_first_collider(ol)
            collision_count+=1
            amount=self.resolve_collision(c)
            if amount>KILL_THRESHHOLD:
                self.die("Looks like you got squished!")
            if collision_count>=3:
                #print("Reached our collision limit")
                break
            c=self.get_first_collider(ol)

        self.ground = self.on_ground(ol)

        #velocity enactment
        self.bounds[0] = vec_add(self.bounds[0], self.vel)



'''
Notes about Player

Elasticity:
    Elasticity for the player sits at one of two values:
    PLAYER_ELASTICITY_CONTROLLED and PLAYER_ELASTICITY_BOUNCY. By
    default, the player is in controlled mode, where she quickly
    comes to a stop on floors. When bouncy, she retains most of her
    energy in a bounce off the floor. 
    
    The value in each is determined by case:
        If the appropriate key is pressed (LSHIFT), BOUNCY
        If the player is colliding in a jumpable fashion and UP is pressed, BOUNCY
        Otherwise, CONTROLLED
        
'''
class Player(Dynamic):
    
    def __init__(self, position):
        super().__init__([position, PLAYER_DIM], 1)
        self.vel = [0,0]
        self.color = PLAYER_COLOR
        self.elasticity = PLAYER_ELASTICITY_CONTROLLED
        self.friction=WALL_FRICTION
        self.ground = None
        self.frictioned = False  #Flag to prevent more than one underfoot platform from each slowing you.

    def do_step(self, ol):
        self.frictioned = False
        #Determine if she stands on something, and what it is
        self.ground = self.on_ground(ol)
        #if she is...
        if self.ground:
            #If the difference in the velocity of player is similar to
            #what she stands on, then set them equal.
            if abs(self.vel[1]-self.ground.vel[1]) < GROUNDING_SPEED:
                self.vel[1] = self.ground.vel[1]
        #Otherwise, If she's in the air...
        else:
            #Enact gravity if in the air.
            self.vel = vec_add(self.vel, GRAVITY)
            #air friction
            self.vel = vec_multiple(self.vel, AIR_FRICTION)
            #Controlling jump height on the ascent
            if not (keys[UP] or keys[LSHIFT]) and self.vel[1]<0:
                self.vel[1]*= JUMP_HALT_FRICTION
            
        #Fundamental movement
        if keys[LEFT]: 
            ro=self.right_of(ol)
            if ro and abs(ro.vel[X]-self.vel[X])<1:
                self.bounds[POS][X] = ro.bounds[POS][X]+ro.bounds[DIM][W]
                self.vel[X]=0
            else:
                if self.ground:      self.vel=vec_add(self.vel, [-WALK_ACCEL,0])
                elif self.vel[X]>-2: self.vel=vec_add(self.vel, [-AIR_ACCEL,0])
        if keys[RIGHT]: 
            lo=self.left_of(ol)
            if lo and abs(lo.vel[X]-self.vel[X])<1:
                self.bounds[POS][X] = lo.bounds[POS][X]-self.bounds[DIM][W]
                self.vel[X]=0
            else:
                if self.ground:     self.vel=vec_add(self.vel, [WALK_ACCEL,0])
                elif self.vel[X]<2: self.vel=vec_add(self.vel, [AIR_ACCEL,0])

            #A bit of airspeed control


        ####################
        #collision handling#
        collision_count=0
        c=self.get_first_collider(ol)
        while c is not None:
            c=self.get_first_collider(ol)
            collision_count+=1
            amount=self.resolve_collision(c)
            if amount>KILL_THRESHHOLD:
                self.die("Looks like you got squished!")
            if collision_count>=3:
                #print("Reached our collision limit")
                break
            c=self.get_first_collider(ol)

        self.ground = self.on_ground(ol)

        #velocity enactment
        self.bounds[0] = vec_add(self.bounds[0], self.vel)

        if self.ground and keys[UP]:
            if isinstance(self.ground, SuperWall):
                new_vel_Y = self.ground.vel[1]-JUMP_SPEED*1.5
            else:
                new_vel_Y = self.ground.vel[1]-JUMP_SPEED
            #Only use the jump velocity if it is faster than our current upward speed (like off a bounce)
            self.vel[Y] = min(self.vel[Y], new_vel_Y)




    def paint_self(self, screen, viewport):
        if self.visible:
            [[x,y],[w,h]] = get_viewport_bounds(self.bounds, viewport)
            pygame.draw.rect(screen, self.color, [x-1,y-1,w+2,h+2], 0)

    def debug_info(self):
        return "Position: "+str(list(map(int, self.bounds[0])))+" Velocity: "+str(self.vel)+" Ground: "+str(None!=self.ground)
        
    def die(self, message):
        #print(message)
        raise FailureException(message)

    def win(self, message):
        print(message)
        raise VictoryException(message)



class Viewport(GameObject):
    
    def __init__(self, bounds, xmove, ymove, following):
        super().__init__(bounds)
        self.solid = False
        self.following = following
        self.vel=[0,0]
        self.xmove=xmove
        self.ymove=ymove
        self.direction=VDOWN #Gravitational AND display direction. TODO this is a physical variable, so it shouldn't be here.

    def do_step(self, ol):
        if self.following:
            if self.xmove:
                self.xmove(self,X)
            if self.ymove:
                self.ymove(self,Y)
        else:
            self.vel=[0,0]

    def paint_self(self, screen, viewport):
        pass        

    def rotate_around_point(self, point, direction):
        [[x,y],[w,h]] = self.bounds
        c = self.center()
        if direction is CW:
            new_center = [c[Y],-c[X]]
            self.vel = [self.vel[Y],-self.vel[X]]
        elif direction is CCW:
            new_center = [-c[Y],c[X]]
            self.vel = [-self.vel[Y],self.vel[X]]
        self.bounds[POS] = vec_add(self.bounds[POS], vec_subtract(new_center, c))

    '''
    Move functions:

    Moves the viewport ALONG ONE AXIS. Different functions can be used on the x
    and y axis to provide fun side-scrolling levels with a fixed y, etc.

    The coordinates are intended to be the centers of the viewport and
    following object. The speeds are magnitudes of the 
    '''
    #Whatever speed the viewport moves, keep doing that
    def viewport_constant(self, axis):
        self.bounds[POS][axis] += self.vel[axis]
    #Always keep follower at center
    def viewport_exact(self, axis):
        self.vel=[0,0]
        [fc,fd] = [self.following.bounds[POS][axis], self.following.bounds[DIM][axis]]
        self.bounds[POS][axis] = fc + fd/2 - self.bounds[DIM][axis]/2
    def viewport_differential(self, axis):
        f = self.following.bounds
        v = self.bounds
        fc = f[POS][axis] + f[DIM][axis]/2
        vc = v[POS][axis] + v[DIM][axis]/2
        speed = (fc - vc) / 15
        self.bounds[POS][axis]+=speed


'''
Methods applying globally?!?
'''

'''
Rotates the world around a point. After the rotation, gravity will still be
downward on the screen
'''
def rotate_objects_around_point(ol, point, direction):
    global display_direction
    if direction is CW:
        display_direction-=1
        display_direction%=4
        for o in ol:
            o.rotate_around_point(point, direction)
    elif direction is CCW:
        display_direction+=1
        display_direction%=4
        for o in ol:
            o.rotate_around_point(point, direction)
    elif direction is FLIP:
        #just rotate twice
        rotate_objects_around_point(ol, point, CCW)
        rotate_objects_around_point(ol, point, CCW)
    else:
        #An absolute direction was given. Use difference and recall with appropriate direction
        if (display_direction-direction)%4 == 3:
            rotate_objects_around_point(ol, point, CCW)
        elif (display_direction-direction)%4 == 1:
            rotate_objects_around_point(ol, point, CW)
        else:
            rotate_objects_around_point(ol, point, FLIP)
