from core.objects import Cell
from core.difinitions import OneDotProblem, Node, AllDotsProblem, State
from core.algorithms import breadth_fs
from random import randint

# colors
black = color(0, 0, 0)
green = color(0, 255, 0)
blue = color(0, 0, 255)
light_blue = color(102, 255, 255)
white = color(255)
red = color(255, 0, 0)
yellow = color(255, 255, 0)

# dimension
num_cells = 20
dimension = 0
screen_size = 800
speed = 100

# global vars
frontier = []
explored = set()
problem = None
start = None
end = None
targets = None
path = []
grid = []
noloop = False
doWhat = 0


def initial_state():
    global grid, dimension, num_cells, start, end, frontier, explored, targets, problem
    # initial the grid
    start = grid[num_cells/2][num_cells/2]
    start.makeit('start')
    end = grid[-1][-1]
    end.makeit('end')
    targets = []
    for i in range(10):
        dot = grid[randint(0, num_cells-1)][randint(0, num_cells-1)]
        dot.makeit('end')
        targets.append(dot)
    frontier = []
    explored.clear()
    # problem = AllDotsProblem(initial=State(start, targets), goal=[], grid=grid)
    problem = OneDotProblem(initial=State(start),
                            goal=State(end), grid=grid)
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
    global grid, speed, frontier, doWhat, problem, explored, noloop
    # calculation
    node, result = breadth_fs(problem, frontier, explored)
    # result check
    if result == 'done' or result == 'failure':
        noLoop()
    # draw grid
    for row in grid:
        for cell in row:
            if cell.isWall:
                cell.show(black)
            elif cell.isStart or cell.isEnd:
                cell.show(yellow)
            else:
                cell.show(white)
    # draw explored
    for s in explored:
        s.cell.show(blue)
    # draw frontier
    for n in frontier:
        cell = n.state.cell
        cell.show(light_blue)
    # draw current
    node.state.cell.show(red)
    # draw path
    if result == "done":
        path = [n.state for n in node.path()]
        for n in path:
            n.cell.show(green)
        print(node.solution())
        print(node.path_cost)


def mouseClicked():
    initial_state()
    loop()
