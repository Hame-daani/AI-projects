from core.objects import Cell
from core.algorithms import astar, breadth_fs, uniform_cost_search
from core import utils
import config
from time import time

# global vars
steps = None
answer = None
step = 0
problem = None
grid = []
algorithms = [breadth_fs, uniform_cost_search, astar]
curr_alg = 0
start_time = 0


def run():
    """
    run algorithm on our problem and saved the result and steps.
    """
    global answer, steps, start_time, algorithms, curr_alg, problem, grid
    # print algorithm name
    print(config.Yellow+"<<" +
          algorithms[curr_alg].__name__+">>"+config.ResetAll)
    # save starting time
    start_time = time()
    # run
    answer, steps = algorithms[curr_alg](problem)


def setup():
    """
    used in processing. run once at start.
    """
    global grid, problem
    # calculate the size of each cell
    w = width / config.column_cells
    h = height / config.row_cells
    # setup display
    size(config.screen_width, config.screen_height)
    frameRate(config.speed)
    # build the grid
    grid = [
        [
            Cell(i, j, w, h) for i in range(config.column_cells)
        ]
        for j in range(config.row_cells)
    ]
    start = utils.build_grid_random(grid)
    # start = utils.biuld_grid_from_file(grid)

    # create our problem to be solved
    problem = utils.create_allDotsProblem(start, grid)
    # run algorithm on our problem
    run()


def draw():
    """
    used in processing. run based on our frameRate in second.
    """
    global grid, step, answer, steps
    # get each step to draw
    node, frontier, explored = steps[step]
    step += 1
    # failure check
    if not answer:
        print(config.Red+"Failure"+config.ResetAll)
        print("Total Time: "+str(config.LightBlue +
                                 "{:.2f}".format(time()-start_time)+config.ResetAll))
        print("Total Nodes: " + config.LightBlue +
              str(len(steps))+config.ResetAll)
        noLoop()
    # success check
    if step == len(steps)-1:
        print(config.Green+"Success"+config.ResetAll)
        print("Total Time: "+str(config.LightBlue +
                                 "{:.2f}".format(time()-start_time)+config.ResetAll))
        print("Total Nodes: " + config.LightBlue +
              str(len(steps))+config.ResetAll)
        print("Total Cost: "+config.LightRed +
              str(answer.path_cost)+config.ResetAll)
        noLoop()
    # draw
    utils.draw_grid(grid)
    utils.draw_explored(explored)
    utils.draw_frontier(frontier)
    # draw current node
    if node:
        node.state.cell.show(config.red)
    # draw answer
    if step == len(steps)-1:
        utils.draw_path(answer)


def mouseClicked():
    """
    change algorithm everythme we clicked the frame.
    """
    global algorithms, curr_alg, step
    curr_alg = (curr_alg+1) % len(algorithms)
    step = 0
    print("")
    run()
    loop()
