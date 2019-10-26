from core.objects import Cell
from core.difinitions import Node, PriorityQueue
from core.algorithms import astar
from random import randint, uniform
from core import utils
from config import *


# global vars
frontier = None
explored = set()
problem = None
grid = []
dimension = 0


def initial_state():
    """
    initialize the state of program.
    """
    global frontier, explored, problem
    # clear our frontier and explored
    frontier = PriorityQueue('min', problem.h)
    explored.clear()
    # add start node to frontier
    frontier.append(Node(state=problem.initial_state))


def setup():
    """
    used in processing. run once at start.
    """
    global screen_size, grid, dimension, problem
    dimension = width / num_cells
    # build the grid
    grid = [
        [
            Cell(i, j, dimension) for i in range(num_cells)
        ]
        for j in range(num_cells)
    ]
    # choose start point
    start = grid[num_cells/2][num_cells/2]
    start.makeit('start')
    # create our problem to be solved
    problem = utils.create_allDotsProblem(start, grid)
    initial_state()
    size(screen_size, screen_size)
    frameRate(speed)


def draw():
    """
    used in processing. run based on our frameRate in second.
    """
    global grid, frontier, problem, explored
    # calculation
    node, result = astar(problem, frontier, explored)
    # result check
    if result == 'done' or result == 'failure':
        print(result)
        noLoop()
    # draw
    utils.draw_grid(grid)
    utils.draw_explored(explored)
    utils.draw_frontier(frontier)
    # draw current node
    if result != "failure":
        node.state.cell.show(red)
    if result == "done":
        utils.draw_path(node)


def mouseClicked():
    initial_state()
    loop()
