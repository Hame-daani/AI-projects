from core.objects import Cell
from core.algorithms import astar, breadth_fs, uniform_cost_search
from core import utils
from config import column_cells, row_cells, speed, screen_height, screen_width, red
from time import time

# global vars
steps = None
answer = None
curr = 0
problem = None
grid = []
algorithms = [breadth_fs, uniform_cost_search, astar]
curr_alg = 0
start_time = 0

ResetAll = "\033[0m"
Black = "\033[30m"
Red = "\033[31m"
Green = "\033[32m"
Yellow = "\033[33m"
Blue = "\033[34m"
Magenta = "\033[35m"
Cyan = "\033[36m"
LightGray = "\033[37m"
DarkGray = "\033[90m"
LightRed = "\033[91m"
LightGreen = "\033[92m"
LightYellow = "\033[93m"
LightBlue = "\033[94m"
LightMagenta = "\033[95m"
LightCyan = "\033[96m"
White = "\033[97m"


def run():
    """
    run algorithm on our problem and saved the result and steps.
    """
    global answer, steps, start_time

    print(Yellow+"<<"+algorithms[curr_alg].__name__+">>"+ResetAll)

    start_time = time()
    answer, steps = algorithms[curr_alg](problem)


def setup():
    """
    used in processing. run once at start.
    """
    global grid, problem

    w = width / column_cells
    h = height / row_cells
    size(screen_width, screen_height)
    frameRate(speed)

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

    run()


def draw():
    """
    used in processing. run based on our frameRate in second.
    """
    global grid, curr, answer, steps

    # calculation
    node, frontier, explored = steps[curr]
    curr += 1
    if not answer:
        print(Red+"Failure"+ResetAll)
        print("Total Time: "+str(LightBlue +
                                 "{:.2f}".format(time()-start_time)+ResetAll))
        print("Total Nodes: " + LightBlue+str(len(steps))+ResetAll)
        noLoop()
    if curr == len(steps)-1:
        print(Green+"Success"+ResetAll)
        print("Total Time: "+str(LightBlue +
                                 "{:.2f}".format(time()-start_time)+ResetAll))
        print("Total Nodes: " + LightBlue+str(len(steps))+ResetAll)
        noLoop()

    # draw
    utils.draw_grid(grid)
    utils.draw_explored(explored)
    utils.draw_frontier(frontier)

    # draw current node
    if node:
        node.state.cell.show(red)

    # draw answer
    if answer and curr == len(steps)-1:
        print("Total Cost: "+LightRed+str(answer.path_cost)+ResetAll)
        utils.draw_path(answer)


def mouseClicked():
    """
    change algorithm everythme we clicked the frame.
    """
    global algorithms, curr_alg, curr
    curr_alg = (curr_alg+1) % len(algorithms)
    curr = 0
    print("")
    run()
    loop()
