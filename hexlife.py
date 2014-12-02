import random
from constants import LIFE_DELAY, DEAD

RULES = {
        (0, 0) : 0,
        (0, 1) : 0,
        (0, 2) : 0.1,
        (0, 3) : 1,
        (0, 4) : 0.1,
        (0, 5) : 0,
        (0, 6) : 0,

        (1, 0) : 0,
        (1, 1) : 0.5,
        (1, 2) : 1,
        (1, 3) : 0.8,
        (1, 4) : 0.2,
        (1, 5) : 0.2,
        (1, 6) : 0,
        }

def get_color(state, live_color):
    if random.random() <= state:
        return live_color
    else:
        return DEAD

def count_alive(cells, live_color):
    return sum([1 for c in cells if c.color == live_color])

def evolve_grid(grid, redraw_cell, live_color, counter=[0]):
    counter[0] += 1
    if counter[0] % LIFE_DELAY != 0:
        return

    new_grid = {}
    for cell in grid.cells():
        new_grid[cell.pos] = RULES[(
            count_alive([cell], live_color), 
            count_alive(grid.neighborhood(cell), live_color))]
    for pos, state in new_grid.items():
        new_color = get_color(state, live_color)
        if grid[pos].color != new_color:
            if grid[pos].color != DEAD and grid[pos].color != live_color:
                # not handling this color right now
                continue
            grid[pos].color = new_color
            redraw_cell(grid[pos])
        

