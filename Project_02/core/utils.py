black = color(0, 0, 0)
green = color(0, 255, 0)
blue = color(0, 0, 255)
light_blue = color(102, 255, 255)
white = color(255)
red = color(255, 0, 0)
yellow = color(255, 255, 0)


def draw_path(node):
    path = [n.state for n in node.path()]
    for n in path:
        n.cell.show(green)
    print(node.solution())
    print(node.path_cost)


def draw_frontier(frontier):
    for i,n in frontier:
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


def create_oneDotProblem(start, grid):
    from core.difinitions import OneDotProblem, State
    end = grid[-1][-1]
    end.makeit('end')
    problem = OneDotProblem(initial=State(start), goal=State(end), grid=grid)
    return problem


def create_allDotsProblem(start, num_cells, grid):
    from core.difinitions import AllDotsProblem, State
    from random import randint
    targets = []
    for i in range(4):
        dot = grid[randint(0, num_cells-1)][randint(0, num_cells-1)]
        dot.makeit('end')
        targets.append(dot)
    problem = AllDotsProblem(initial=State(start, targets), goal=[], grid=grid)
    return problem
