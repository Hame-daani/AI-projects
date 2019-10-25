from core.objects import Cell
from core.algorithms import dfs, bfs, heuristic, astar

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
speed = 10

# global vars
frontier = []
start = None
dots = None
end = None
path = []
grid = []
doWhat = 0


def initial_state():
    global grid, dimension, num_cells, start, end, frontier,dots
    # initial the grid
    start = grid[num_cells/2][num_cells/2]
    end = grid[-1][-1]
    start.makeit('start')
    end.makeit('end')
    frontier = []
    frontier.append(start)

def setup():
    global screen_size, grid, dimension
    dimension = width / num_cells
    grid = [[Cell(i, j, dimension) for j in range(num_cells)]
            for i in range(num_cells)]
    initial_state()
    size(screen_size, screen_size)
    frameRate(speed)


def draw():
    global grid, speed, frontier, doWhat
    # calculation
    # result check
    # draw grid
    for row in grid:
        for cell in row:
            if cell.isWall:
                cell.show(black)
            elif cell.explored:
                cell.show(blue)
            elif cell.isStart or cell.isEnd:
                cell.show(yellow)
            else:
                cell.show(white)
    # draw path
    # draw frontier


def mouseClicked():
    initial_state()
    global doWhat
    doWhat = (doWhat+1) % 3
    if doWhat == 0:
        print("BFS")
    if doWhat == 1:
        print("DFS")
    if doWhat == 2:
        print("Astar")
    loop()
