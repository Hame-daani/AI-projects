from config import *


def draw_path(node):
    """
    draw a green path as our solution.
    """
    path = [n.state for n in node.path()]
    for n in path:
        n.cell.show(green)
    print(node.solution())


def draw_frontier(frontier):
    """
    draw our frontier in current state.
    """
    for n in frontier:
        if type(n) == tuple:
            i, n = n
        cell = n.state.cell
        cell.show(light_blue)


def draw_explored(explored):
    """
    draw explored cells.
    """
    for s in explored:
        s.cell.show(blue)


def draw_grid(grid):
    """
    draw our grid based on what cell is.
    """
    for row in grid:
        for cell in row:
            if cell.isWall:
                cell.show(black)
            elif cell.isStart or cell.isEnd:
                cell.show(yellow)
            else:
                cell.show(white)


def create_allDotsProblem(start, grid):
    """
    Get a start point and grid, and return a problem with randm dots as targets.
    """
    from core.difinitions import AllDotsProblem, State
    from random import randint
    targets = []
    for row in grid:
        for cell in row:
            if cell.isEnd:
                targets.append(cell)
    problem = AllDotsProblem(initial=State(start, targets), grid=grid)
    return problem


def biuld_grid_from_file(grid):
    start = None
    with open("input.txt") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        for j, num in enumerate(line.rstrip().split()):
            if num == '0':
                start = grid[i][j]
                start.makeit("start")
            elif num == '-1':
                grid[i][j].isWall = True
            elif num == '-2':
                grid[i][j].makeit('end')
            else:
                grid[i][j].weight = int(num)
    return start


def build_grid_random(grid):
    from random import randint, uniform
    # create walls and give them weights
    for row in grid:
        for cell in row:
            cell.weight = randint(1, 10)
            if uniform(0, 1) < 0.2:
                cell.isWall = True
    # choose center as start
    start = grid[row_cells/2][column_cells/2]
    start.makeit('start')
    # choose random targets
    for i in range(num_dots):
        dot = start
        while dot == start:
            dot = grid[randint(0, row_cells-1)][randint(0, column_cells-1)]
        dot.makeit('end')
    return start
