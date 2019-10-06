from core.objects import Cell
from core.algorithms import bfs

# colors
black = color(0, 0, 0)
green = color(0, 255, 0)
blue = color(0, 0, 255)
light_blue = color(102, 255, 255)
white = color(255)
red = color(255, 0, 0)
yellow = color(255, 255, 0)

# dimension
num_cells = 10
dimension = 0
screen_size = 500
speed = 10

# global vars
frontier = []
start = None
end = None
path = []
grid = []


def setup():
    global screen_size, grid, dimension, start, end
    dimension = width / num_cells
    grid = [[Cell(i, j, dimension) for j in range(num_cells)]
            for i in range(num_cells)]
    start = grid[0][0]
    end = grid[num_cells-1][num_cells-1]
    size(screen_size, screen_size)


def draw():
    global grid, speed
    frameRate(speed)
    # show grid
    for row in grid:
        for cell in row:
            cell.show(white)
    # show start and end
    start.show(green)
    end.show(red)
