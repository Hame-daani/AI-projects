from core.objects import Cell
from core.difinitions import Node, PriorityQueue
from core.algorithms import astar, breadth_fs, uniform_cost_search
from random import randint, uniform
from core import utils
from config import *


# global vars
frontier = None
explored = set()
problem = None
grid = []
dimension = 0
total_nodes = 0
algorithms = [breadth_fs, uniform_cost_search, astar]
curr_alg = 0


def initial_state():
    """
    initialize the state of program.
    """
    global frontier, explored, problem, algorithms, curr_alg, total_nodes
    total_nodes = 0
    # clear our frontier and explored
    if algorithms[curr_alg] == astar:
        frontier = PriorityQueue('min', lambda n: n.path_cost+problem.h(n))
    elif algorithms[curr_alg] == uniform_cost_search:
        frontier = PriorityQueue('min', lambda n: n.path_cost)
    else:
        frontier = []
    explored.clear()
    # add start node to frontier
    frontier.append(Node(state=problem.initial_state))


def setup():
    """
    used in processing. run once at start.
    """
    global screen_size, grid, dimension, problem, algorithms, curr_alg
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
    print(algorithms[curr_alg].__name__)


def draw():
    """
    used in processing. run based on our frameRate in second.
    """
    global grid, frontier, problem, explored, total_nodes, algorithms, curr_alg
    # calculation
    node, result = algorithms[curr_alg](problem, frontier, explored)
    total_nodes += 1
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
        print("Total Nodes: " + str(total_nodes))
        print("Total Cost: "+str(node.path_cost))
        utils.draw_path(node)


def mouseClicked():
    global algorithms, curr_alg
    curr_alg = (curr_alg+1) % len(algorithms)
    initial_state()
    print("")
    print(algorithms[curr_alg].__name__)
    loop()
