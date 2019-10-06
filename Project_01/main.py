from core.objects import Cell
from core.algorithms import bfs

# colors
# pylint: disable=undefined-variable
black = color(0, 0, 0)
green = color(0, 255, 0)
blue = color(0, 0, 255)
light_blue = color(102, 255, 255)
white = color(255)
red = color(255, 0, 0)
yellow = color(255, 255, 0)
# pylint: enable=undefined-variable

# dimension
num_cells = 20
dimension = 0
screen_size = 500
speed = 100

# global vars
frontier = []
start = None
end = None
path = []
grid = [[Cell(i, j) for j in range(num_cells)] for i in range(num_cells)]


def setup():
    pass


def draw():
    pass
