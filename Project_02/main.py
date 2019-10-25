from core.objects import Cell
from core.difinitions import OneDotProblem, Node
from core.algorithms import breadth_fs

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
dots = None
end = None
path = []
grid = []
noloop = False
doWhat = 0


def initial_state():
    global grid, dimension, num_cells, start, end, frontier, explored, dots, problem
    # initial the grid
    start = grid[num_cells/2][num_cells/2]
    end = grid[-1][-1]
    start.makeit('start')
    end.makeit('end')
    frontier = []
    explored.clear()
    problem = OneDotProblem(initial=start, goal=end, grid=grid)
    frontier.append(Node(state=start))


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
    for cell in explored:
        cell.show(blue)
    # draw frontier
    for n in frontier:
        cell = n.state
        cell.show(light_blue)
    # draw current
    node.state.show(red)
    # draw path
    if result == "done":
        path = [n.state for n in node.path()]
        for cell in path:
            cell.show(green)
        print(node.solution())


def mouseClicked():
    initial_state()
    loop()
