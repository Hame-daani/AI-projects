from config import *


def draw_path(node):
    path = [n.state for n in node.path()]
    for n in path:
        n.cell.show(green)
    print(node.solution())
    print(node.path_cost)


def draw_frontier(frontier):
    for i, n in frontier:
        cell = n.state.cell
        cell.show(light_blue)


def draw_explored(explored):
    for s in explored:
        s.cell.show(blue)


def draw_grid(grid):
    for row in grid:
        for cell in row:
            if cell.isWall:
                cell.show(black)
            elif cell.isStart or cell.isEnd:
                cell.show(yellow)
            else:
                cell.show(white)


def create_allDotsProblem(start, grid):
    from core.difinitions import AllDotsProblem, State
    from random import randint
    targets = []
    for i in range(num_dots):
        dot = grid[randint(0, num_cells-1)][randint(0, num_cells-1)]
        dot.makeit('end')
        targets.append(dot)
    problem = AllDotsProblem(initial=State(start, targets), grid=grid)
    return problem
