class Problem:
    def __init__(self, initial, goal=None):
        self.initial_state = initial
        self.goal = goal

    def goal_test(self, state):
        return self.goal == state

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def step_cost(self, current_cost, fRom, action, to):
        return current_cost+1


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_cost = problem.step_cost(
            self.path_cost, fRom=self.state, action=action, to=next_state)
        next_node = Node(state=next_state, parent=self,
                         action=action, path_cost=next_cost)
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node = self
        path = []
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))
    # buit_in functions

    def __eq__(self, value):
        return isinstance(value, Node) and self.state == value.state

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __hash__(self):
        return hash(self.state)


class OneDotProblem(Problem):
    def __init__(self, initial, goal=None, grid=[]):
        Problem.__init__(self, initial, goal)
        self.grid = grid

    def actions(self, state):
        cell = state.cell
        possible_acts = ["UP", "DOWN", "RIGHT", "LEFT"]
        if cell.i == 0 or self.grid[cell.j][cell.i-1].isWall:
            possible_acts.remove("LEFT")
        if cell.j == 0 or self.grid[cell.j-1][cell.i].isWall:
            possible_acts.remove("UP")
        if cell.i == len(self.grid)-1 or self.grid[cell.j][cell.i+1].isWall:
            possible_acts.remove("RIGHT")
        if cell.j == len(self.grid)-1 or self.grid[cell.j+1][cell.i].isWall:
            possible_acts.remove("DOWN")
        return possible_acts

    def result(self, state, action):
        old_i = state.cell.i
        old_j = state.cell.j
        if action == "UP":
            return State(self.grid[old_j-1][old_i])
        if action == "DOWN":
            return State(self.grid[old_j+1][old_i])
        if action == "RIGHT":
            return State(self.grid[old_j][old_i+1])
        if action == "LEFT":
            return State(self.grid[old_j][old_i-1])

    def step_cost(self, current_cost, fRom, action, to):
        return current_cost + to.cell.weight


class State:
    def __init__(self, cell, targets=[]):
        self.cell = cell
        self.targets = targets

    def __eq__(self, value):
        return self.cell == value.cell and self.targets == value.targets

    def __hash__(self):
        return hash((self.cell, frozenset(*self.targets)))


class AllDotsProblem(OneDotProblem):
    def __init__(self, initial, goal=None, grid=[]):
        OneDotProblem.__init__(self, initial, goal=goal, grid=grid)

    def result(self, state, action):
        cell, targets = state.cell, state.targets
        old_i = cell.i
        old_j = cell.j
        if action == "UP":
            new_cell = self.grid[old_j-1][old_i]
        if action == "DOWN":
            new_cell = self.grid[old_j+1][old_i]
        if action == "RIGHT":
            new_cell = self.grid[old_j][old_i+1]
        if action == "LEFT":
            new_cell = self.grid[old_j][old_i-1]
        new_targets = targets[:]
        if new_cell in new_targets:
            new_targets.remove(new_cell)
        return State(new_cell, new_targets)

    def goal_test(self, state):
        return self.goal == state.targets
