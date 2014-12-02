"""
author: jakob.erdmann@gmail.com
license: GPL 3.0 or newer
"""
from vector2D import Vec2d

GRIDDIM = Vec2d(32,32)
FIELDSIZE = 32

LIFE_DELAY = 5

# colors
DEAD = (255, 0, 0)
ALIVE1 = (0, 255, 0)
ALIVE2 = (0, 0, 255)

COLORCYCLE = [DEAD, ALIVE1, ALIVE2]
