import pygame

#########################
##Game constants
FPS = 59                            #Frames per second (both graphical and operational
SCREEN_DIM = (700,520)              #Dimensions of the window
CDIM = [16,16]                      #Dimensions of a "cell" on the screen. Needs some work
GRAVITY = [0,1000/FPS**2]           #Gravity vector (horizontal gravity is not supported)
AIR_FRICTION = 1                    #Friction when not on ground
PLAYER_ELASTICITY_BOUNCY=.9         #Elasticity (bounciness) when bounce key is pressed
PLAYER_ELASTICITY_CONTROLLED=.15    #Your elasticity when it is controlled (normal)
PLAYER_DIM=[30,30]
WALL_ELASTICITY=.85                 
WALL_FRICTION=.83                   #Friction when walking on normal ground
GROUNDING_SPEED=100/FPS             #Allowed differential for when you lock into the ground speed
JUMP_SPEED = 475/FPS                #How hard you jump
JUMP_HALT_FRICTION = .85            #Friction which brings you to a stop in a midair jump after releasing UP
WALK_ACCEL = 40/FPS                 #How fast you walk
AIR_ACCEL = 2.5/FPS                 #Left/Right control in midair
KILL_THRESHHOLD=2                   #How much "crunch" you take before dying
SUPER_WALL_ELASTICITY=1.5
SUPER_WALL_HORIZONTAL_ELASTICITY=3

#######################
##Derived constants, very useful in constructing levels
def get_walk_speed(accel, friction):
    #Shortcut: instead of iterating, find the max:
    return accel/(1-friction)
    #This max is approached by the below iteration:
    '''
    speed=0
    for i in range(XXX):
        speed*=friction
        speed+=accel
    return speed
    '''

def get_jump_height(vspeed, grav, air_friction):
    jh=0
    while vspeed<0:
        if jh is not 0: 
            vspeed+=grav
            vspeed*=air_friction
        if vspeed<0: jh+= -1*vspeed
    return jh

#absolute max, edge-to-edge jumpable chasm width
def get_jump_distance(hspeed, vspeed, grav, air_friction):
    x=0
    y=0
    while y<=0:
        vspeed+=grav
        vspeed*=air_friction
        if y<=0:
            y+=vspeed
            x+=hspeed
    return x+PLAYER_DIM[1]
    
WALK_SPEED=                 get_walk_speed(WALK_ACCEL, WALL_FRICTION)
JUMP_DISTANCE=              get_jump_distance(WALK_SPEED, -JUMP_SPEED, GRAVITY[1], AIR_FRICTION)
JUMP_HEIGHT=                get_jump_height(-JUMP_SPEED, GRAVITY[1], AIR_FRICTION)
SUPER_WALL_JUMP_HEIGHT=     get_jump_height(-JUMP_SPEED*SUPER_WALL_ELASTICITY, GRAVITY[1], AIR_FRICTION)

#print("WALK_SPEED =",WALK_SPEED)
#print("JUMP_DISTANCE =",JUMP_DISTANCE)
#print("JUMP_HEIGHT =",JUMP_HEIGHT)
#print("SUPER_WALL_JUMP_HEIGHT =",SUPER_WALL_JUMP_HEIGHT)

##########
#INDEX CONSTANTS
RIGHT   =pygame.K_RIGHT
DOWN    =pygame.K_DOWN
LEFT    =pygame.K_LEFT
UP      =pygame.K_UP

LSHIFT  =pygame.K_LSHIFT
RETURN  =pygame.K_RETURN
K_W     =pygame.K_w
K_R     =pygame.K_r
K_X     =pygame.K_x
K_P     =pygame.K_p
K_K     =pygame.K_k
K_F     =pygame.K_f
K_S     =pygame.K_s



POS=0
DIM=1
X=0
Y=1
W=0
H=1

VDOWN = 0
VRIGHT = 1
VUP = 2
VLEFT = 3

CW = 4
CCW = 5
FLIP = 6

#Initializations
keys=[]
MOUSEPOS = [-1,-1]

###########
#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
PINK = (255,180,180)
GRAY = (100,100,100)

BACK_COLOR = (20,20,20)
PLAYER_COLOR = (100,200,255)
PLATFORM_COLOR = YELLOW 
WALL_COLOR = GRAY
KILLER_COLOR = (255, 100, 100)
SUPER_WALL_COLOR = BLUE
FINISH_COLOR = GREEN
BUTTON_COLOR = MAGENTA
DYNAMIC_COLOR = (100,100,30)

def vec_add(v1, v2):
    return list(map(sum, zip(v1,v2)))

def vec_subtract(v1, v2):
    return vec_add(v1, vec_invert(v2))

def bounds_overlap(a,b):
    [ax1,ay1]=a[0]
    [ax2,ay2]=vec_add(a[0],a[1])
    [bx1,by1]=b[0]
    [bx2,by2]=vec_add(b[0],b[1])
    return (ax1 < bx2) and (bx1 < ax2) and (ay1 < by2) and (by1 < ay2)

def shift_bounds_static(bound, vec):
        return [vec_add(bound[0],vec), bound[1]]

def vec_multiple(v, c):
    return list(map(lambda x: c*x, v))

def vec_invert(v):
    return vec_multiple(v,-1)

def vec_length(v):
    return sum(map(lambda x: x*x, v))**.5

def get_viewport_coordinates(p, viewport):
    [x,y]=p
    [[vx,vy],[vw,vh]]=viewport.bounds
    nx=(x-vx) * SCREEN_DIM[W]/vw
    ny=(y-vy) * SCREEN_DIM[H]/vh
    return [nx,ny]

def get_viewport_bounds(bounds, viewport):
    [[x,y],[w,h]]=bounds
    [[vx,vy],[vw,vh]]=viewport.bounds
    nx=(x-vx) * SCREEN_DIM[W]/vw
    ny=(y-vy) * SCREEN_DIM[H]/vh
    nw= w     * SCREEN_DIM[W]/vw
    nh= h     * SCREEN_DIM[H]/vh
    return [[nx,ny],[nw,nh]]

def get_absolute_coordinates(screen_point, viewport):
    [sx,sy] = screen_point
    [[vx,vy],[vw,vh]] = viewport.bounds
    [sw,sh] = SCREEN_DIM
    return [vx + (sx/sw * vw), vy + (sy/sh * vh)]

class VictoryException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class FailureException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

