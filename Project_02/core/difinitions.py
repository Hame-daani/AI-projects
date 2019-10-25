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


class OneDotProblem(Problem):
    def __init__(self, initial, goal=None, grid=[]):
        Problem.__init__(self, initial, goal)
        self.grid = grid

    def actions(self, state):
        possible_acts = ["UP", "DOWN", "RIGHT", "LEFT"]
        if state.i == 0 or self.grid[state.j][state.i-1].isWall:
            possible_acts.remove("LEFT")
        if state.j == 0 or self.grid[state.j-1][state.i].isWall:
            possible_acts.remove("UP")
        if state.i == len(self.grid)-1 or self.grid[state.j][state.i+1].isWall:
            possible_acts.remove("RIGHT")
        if state.j == len(self.grid)-1 or self.grid[state.j+1][state.i].isWall:
            possible_acts.remove("DOWN")
        return possible_acts

    def result(self, state, action):
        old_i = state.i
        old_j = state.j
        if action == "UP":
            return self.grid[old_j-1][old_i]
        if action == "DOWN":
            return self.grid[old_j+1][old_i]
        if action == "RIGHT":
            return self.grid[old_j][old_i+1]
        if action == "LEFT":
            return self.grid[old_j][old_i-1]

    def step_cost(self, current_cost, fRom, action, to):
        return current_cost + to.weight
