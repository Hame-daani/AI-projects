from core.objects import Cell
from core.difinitions import Node
from core.algorithms import astar, breadth_fs, uniform_cost_search, iterative_deeping_search
from core import utils
from config import column_cells, row_cells, speed, screen_height, screen_width, red
import time

# global vars
frontier = None
explored = set()
problem = None
grid = []
algorithms = [astar, uniform_cost_search,
              breadth_fs,  iterative_deeping_search]
total_nodes = 0
curr_alg = 0
start_time = 0


def initial_state():
    """
    initialize the state of program.
    """
    global frontier, explored, problem, algorithms, curr_alg, total_nodes, start_time
    total_nodes = 0
    start_time = time.time()
    # clear our frontier and explored
    if algorithms[curr_alg] == astar:
        frontier = utils.PriorityQueue(
            'min', lambda n: n.path_cost+problem.h(n))
    elif algorithms[curr_alg] == uniform_cost_search:
        frontier = utils.PriorityQueue('min', lambda n: n.path_cost)
    else:
        frontier = []
    explored.clear()
    # add start node to frontier
    frontier.append(Node(state=problem.initial_state))


def setup():
    """
    used in processing. run once at start.
    """
    global grid, problem, algorithms, curr_alg
    w = width / column_cells
    h = height / row_cells

    # build the grid
    grid = [
        [
            Cell(i, j, w, h) for i in range(column_cells)
        ]
        for j in range(row_cells)
    ]

    start = utils.build_grid_random(grid)
    # start = utils.biuld_grid_from_file(grid)

    # create our problem to be solved
    problem = utils.create_allDotsProblem(start, grid)
    initial_state()
    size(screen_width, screen_height)
    frameRate(speed)
    print("<<"+algorithms[curr_alg].__name__+">>")


def draw():
    """
    used in processing. run based on our frameRate in second.
    """
    global grid, frontier, problem, explored, total_nodes, algorithms, curr_alg, start_time
    # draw
    utils.draw_grid(grid)
    # calculation
    node, result = algorithms[curr_alg](problem, frontier, explored)
    total_nodes += 1
    # result check
    if result == 'done' or result == 'failure':
        print(result)
        noLoop()
    # draw
    utils.draw_explored(explored)
    utils.draw_frontier(frontier)
    # draw current node
    if result != "failure":
        node.state.cell.show(red)
    if result == "done":
        print("Total Nodes: " + str(total_nodes))
        print("Total Cost: "+str(node.path_cost))
        print("Total time: ")+str(time.time()-start_time)
        utils.draw_path(node)


def mouseClicked():
    global algorithms, curr_alg
    curr_alg = (curr_alg+1) % len(algorithms)
    initial_state()
    print("")
    print("<<"+algorithms[curr_alg].__name__+">>")
    loop()
