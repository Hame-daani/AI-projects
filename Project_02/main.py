from core.objects import Cell
from core.difinitions import OneDotProblem, Node, AllDotsProblem, State, PriorityQueue
from core.algorithms import breadth_fs, astar
from random import randint
from core import utils
from config import *


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

    problem = utils.create_allDotsProblem(start, grid)

    frontier = PriorityQueue('min', problem.h)
    explored.clear()
    frontier.append(Node(state=problem.initial_state))


def setup():
    global screen_size, grid
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
    global grid, frontier, problem, explored
    # calculation
    node, result = astar(problem, frontier, explored)
    # result check
    if result == 'done' or result == 'failure':
        print(result)
        noLoop()
    # draw grid
    utils.draw_grid(grid)
    # draw explored
    utils.draw_explored(explored)
    # draw frontier
    utils.draw_frontier(frontier)
    # draw current
    if result != "failure":
        node.state.cell.show(red)
    # draw path
    if result == "done":
        utils.draw_path(node)


def mouseClicked():
    initial_state()
    loop()
