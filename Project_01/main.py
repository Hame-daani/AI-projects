from core.objects import Cell
from core.algorithms import dfs, bfs

# colors
black = color(0, 0, 0)
green = color(0, 255, 0)
blue = color(0, 0, 255)
light_blue = color(102, 255, 255)
white = color(255)
red = color(255, 0, 0)
yellow = color(255, 255, 0)

# dimension
num_cells = 10
dimension = 0
screen_size = 500
speed = 10

# global vars
frontier = []
start = None
end = None
path = []
grid = []


def initial_state():
    global grid, dimension, num_cells, start, end, frontier
    # create grid
    grid = [[Cell(i, j, dimension) for j in range(num_cells)]
            for i in range(num_cells)]
    # add neighbors for each cell
    for row in grid:
        for c in row:
            c.addNeighbors(grid, num_cells)
    # choose start
    start = grid[0][0]
    start.isWall = False
    start.isStart = True
    # choose end
    end = grid[num_cells-1][num_cells-1]
    end.isWall = False
    end.isEnd = True
    frontier = []
    # initial frontier with start
    frontier.append(start)


def setup():
    global screen_size, grid, dimension, start, end
    dimension = width / num_cells
    initial_state()
    size(screen_size, screen_size)


def draw():
    global grid, speed, frontier
    frameRate(speed)
    # calculation
    current, result = bfs(frontier, end)
    if result == "done" or result == "failure":
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
        path.append(temp)
        temp = temp.previous
    if current == end:
        print(path)
    for x in path:
        x.show(green) if result == "done" else x.show(yellow)
    # draw frontier
    for f in frontier:
        f.show(light_blue)


def mouseClicked():
    # BUG: not work when last done
    initial_state()
    redraw()
