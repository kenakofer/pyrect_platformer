# pyrect_platformer

Platforming game in pygame, with precision control and good frame-of-reference physics for single actor. Simple rectangular layout and graphics, cause that's all you need.

## Running

+ Requires python3 with pygame
+ Level editor: `./level_design.py`
+ Game: `./main.py`

## Gameplay

+ ARROWS to move left, right, and jump
+ SHIFT to increase elasticity (bounciness)
+ R to restart the level
+ Reach the green goal object to complete the level
+ Avoid red killers, use yellow moving platforms, step on buttons that change the physical world
+ Several levels serve as a demonstration of gameplay possibilities for further development
+ Good frame of reference physics: Am I moving or is the rest of the world?

## Level design

New levels are easily laid out with the level editor, which outputs full python source with a function for the level's creation. Buttons and platforms can be given more dynamic options by editing this python source. Newly created levels must be added to the level queue in `main.py`. The level initialization function exported by the level file can take an arbitrary number of arguments. 

Buttons take functions to alter the state of the world, including speeds, positions, colors, visibilities, gravity directions, and more. They can be made invisible to be more inconspicuous triggers of events.

The viewport has different options for the X and Y axes, including fixed position, centering, and differential speed that can be set on a per-level or intra-level basis.

## Graphics
Colored rectangles. Functionality, speed, and playability is the focus here, not glitz.
