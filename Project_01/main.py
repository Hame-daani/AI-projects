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
screen_size = 500
speed = 10

# global vars
frontier = []
start = None
end = None
path = []
grid = []
doWhat = 0


def initial_state():
    global grid, dimension, num_cells, start, end, frontier
    # create grid
    for row in grid:
        for c in row:
            c.explored = False
            c.neighbors = []
            c.previous = None
            c.isStart = False
            c.isEnd = False
            # for use in astra alg
            c.f = 100000000
            c.g = 100000000
            c.addNeighbors(grid, num_cells)
    # choose start
    start = grid[num_cells/2][num_cells/2]
    start.isWall = False
    start.isStart = True
    start.g = 0
    # choose end
    end = grid[num_cells-1][num_cells-1]
    end.isWall = False
    end.isEnd = True
    start.f = heuristic(start, end)
    frontier = []
    # initial frontier with start
    frontier.append(start)


def setup():
    global screen_size, grid, dimension, start, end
    dimension = width / num_cells
    grid = [[Cell(i, j, dimension) for j in range(num_cells)]
            for i in range(num_cells)]
    initial_state()
    size(screen_size, screen_size)
    frameRate(speed)


def draw():
    global grid, speed, frontier, doWhat
    # calculation
    if doWhat == 0:
        current, result = bfs(frontier, end)
    if doWhat == 1:
        current, result = dfs(frontier, end)
    if doWhat == 2:
        current, result = astar(frontier, end)
    if result == "done" or result == "failure":
        print(result)
        noLoop()
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
    # BUG: sometime not draw green the path
    path = []
    temp = current
    while temp:
        if not temp == end:
            temp.show(green) if result == "done" else temp.show(yellow)
        temp = temp.previous
    # draw frontier
    for f in frontier:
        f.show(light_blue)


def mouseClicked():
    initial_state()
    global doWhat
    doWhat = (doWhat+1) % 3
    if doWhat == 0:
        print("BFS")
    if doWhat == 1:
        print("DFS")
    if doWhat == 1:
        print("Astar")
    loop()
