from core.objects import Cell
from core.algorithms import astar, breadth_fs, uniform_cost_search, iterative_deeping_search
from core import utils
from config import column_cells, row_cells, speed, screen_height, screen_width, red
from time import time

# global vars
steps = None
answer = None
curr = 0
problem = None
grid = []
algorithms = [breadth_fs, uniform_cost_search, astar, iterative_deeping_search]
curr_alg = 0


def run():
    """
    initialize the state of program.
    """
    global answer, steps

    print("<<"+algorithms[curr_alg].__name__+">>")

    start_time = time()
    answer, steps = algorithms[curr_alg](problem)
    print("Total Time: ")+str(time()-start_time)

    if answer:
        print("done.")
    else:
        print("failure")

    print("Total Nodes: " + str(len(steps)))


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
    if curr == len(steps)-1:
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
        print("Total Cost: "+str(answer.path_cost))
        utils.draw_path(answer)


def mouseClicked():
    global algorithms, curr_alg, curr
    curr_alg = (curr_alg+1) % len(algorithms)
    curr = 0
    run()
    loop()
