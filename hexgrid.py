#!/usr/bin/env python
"""
author: jakob.erdmann@gmail.com
license: GPL 3.0 or newer
"""
import os, sys
import pygame
import math
from pygame.locals import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'util'))

from vector2D import Vec2d
from draw import draw_text
from constants import GRIDDIM, FIELDSIZE
#import autopdb

SQRT3 = math.sqrt(3)
SQUASH = 1.5 / SQRT3 


class Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._cells = {}
        for x in range(self.width):
            for y in range(self.height):
                self._cells[(x,y)] = Cell(x, y)

    def cells(self):
        return self._cells.values()

    def neighborhood(self, cell):
        a = 1 if cell.pos.y % 2 == 0 else -1
        res = [
                self._cells.get(cell.pos + (1, 0)),
                self._cells.get(cell.pos + (-1, 0)),
                self._cells.get(cell.pos + (0, 1)),
                self._cells.get(cell.pos + (0, -1)),
                self._cells.get(cell.pos + (a, 1)),
                self._cells.get(cell.pos + (a, -1)),
                ]
        return filter(None, res)


class Cell():
    def __init__(self, x, y, color=(255,0,0)):
        self.pos = Vec2d(x, y)
        self.color = color
        self.color2 = (0, 255, 0)

    def toggle_color(self):
        self.color, self.color2 = self.color2, self.color

def draw_grid(screen, grid):
    for cell in grid.cells():
        draw_cell(screen, cell)

def draw_cell(screen, cell):
    x, y = cell.pos
    center = draw_hex(screen, x, y, cell.color)
    draw_text(screen, center, "%s,%s" % (x, y), 20, (255,255,255))

def get_hex_center(x, y):
    center = (Vec2d(x + 0.5, SQUASH * y + 0.5) * FIELDSIZE).toInt()
    if y % 2 == 0:
        center += (0.5 * FIELDSIZE, 0)
    return center

def draw_hex(screen, x, y, color):
    center = get_hex_center(x, y)
    
    a = FIELDSIZE * 0.5
    h = SQRT3 / 2 * a
    points = (
        center + (0, a),
        center + (-h, 0.5 * a),
        center + (-h, -0.5 * a),
        center + (0, -a),
        center + (h, -0.5 * a),
        center + (h, 0.5 * a))
    pygame.draw.polygon(screen, color, points)
    return center

def clicked_cell(grid, pixelpos):
    # invert position computation in draw_hex(), approximate clickable area by a circle
    px, py = pixelpos
    y = round((py - 0.5 * FIELDSIZE) / (SQUASH * FIELDSIZE))
    if y % 2 == 0:
        px -= (0.5 * FIELDSIZE)
    x = round((px - 0.5 * FIELDSIZE) / FIELDSIZE)

    cell = grid._cells.get((x, y))
    if cell:
        dist = get_hex_center(x, y).get_distance(pixelpos)
        if dist < 0.5 * FIELDSIZE:
            return cell
        else:
            return None
    else:
        return None
    

def handle_click(screen, grid, pixelpos):
    cell = clicked_cell(grid, pixelpos)
    if cell:
        cell.toggle_color()
        draw_cell(screen, cell)

def handle_right_click(screen, grid, pixelpos):
    cell = clicked_cell(grid, pixelpos)
    if cell:
        neighborhood = grid.neighborhood(cell)
        for cell in neighborhood:
            cell.toggle_color()
            draw_cell(screen, cell)

def main():
#Initialize Everything
    pygame.init()

    screen = pygame.display.set_mode((GRIDDIM + (1, 1)) * FIELDSIZE + Vec2d(2,2)
            )#, pygame.FULLSCREEN)
    pygame.display.set_caption('Hexgrid')
    #pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()


#Prepare Objects
    clock = pygame.time.Clock()
    grid = Grid(GRIDDIM.x, GRIDDIM.y)

# draw initially
    draw_grid(screen, grid)

#Main Loop
    while True:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key in (K_ESCAPE, K_q):
                return
            elif event.type == MOUSEBUTTONDOWN: 
                if event.button == 1: # left click
                    handle_click(screen, grid, event.pos)
                elif event.button == 3: # right click
                    handle_right_click(screen, grid, event.pos)


    #Draw Everything
        #screen.blit(last_screen, (0, 0))
        #draw_grid(screen, grid)
        pygame.display.flip()


#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
    main()

