from core.objects import Cell
from core.difinitions import OneDotProblem, Node, AllDotsProblem, State, PriorityQueue
from core.algorithms import breadth_fs, astar
from random import randint
from core import utils

# colors
black = color(0, 0, 0)
green = color(0, 255, 0)
blue = color(0, 0, 255)
light_blue = color(102, 255, 255)
white = color(255)
red = color(255, 0, 0)
yellow = color(255, 255, 0)

# config
num_cells = 50
dimension = 0
screen_size = 800
speed = 100

# global vars
frontier = None
explored = set()
problem = None
grid = []


def initial_state():
    global grid, num_cells, frontier, explored, problem
    # initial the grid
    start = grid[num_cells/2][num_cells/2]
    start.makeit('start')

    problem = utils.create_oneDotProblem(start, grid)

    # problem = utils.create_allDotsProblem(start, num_cells, grid)
    frontier = PriorityQueue('min', problem.h)
    explored.clear()
    frontier.append(Node(state=problem.initial_state))


def setup():
    global screen_size, grid, dimension
    dimension = width / num_cells
    grid = [
        [
            Cell(i, j, dimension) for i in range(num_cells)
        ]
        for j in range(num_cells)
    ]
    initial_state()
    size(screen_size, screen_size)
    frameRate(speed)


def draw():
    global grid, speed, frontier, problem, explored
    # calculation
    node, result = astar(problem, frontier, explored)
    # result check
    if result == 'done' or result == 'failure':
        noLoop()
    # draw grid
    utils.draw_grid(grid)
    # draw explored
    utils.draw_explored(explored)
    # draw frontier
    utils.draw_frontier(frontier)
    # draw current
    node.state.cell.show(red)
    # draw path
    if result == "done":
        utils.draw_path(node)


def mouseClicked():
    initial_state()
    loop()
