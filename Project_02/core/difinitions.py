from core.utils import row_cells, column_cells, PriorityQueue


class Problem(object):
    """
    Base class for our problems.
    """

    def __init__(self, initial, goal=None):
        self.initial_state = initial
        self.goal = goal

    def goal_test(self, state):
        return self.goal == state

    def actions(self, state):
        """
        returns all the possible actions from the given state.
        """
        raise NotImplementedError

    def result(self, state, action):
        """
        returns the result state from the given state using the given action.
        """
        raise NotImplementedError

    def step_cost(self, current_cost, fRom, action, to):
        """
        cost to from 'fRom' to 'to' with the 'action'
        """
        return current_cost+1


class Node:
    """
    Node class to hold current state and action and cost that it take.
    """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def child_node(self, problem, action):
        """
        returns a node that build from current node in this 'problem' whit this 'action'
        """
        next_state = problem.result(self.state, action)
        next_cost = problem.step_cost(
            self.path_cost, fRom=self.state, action=action, to=next_state)
        next_node = Node(state=next_state, parent=self,
                         action=action, path_cost=next_cost)
        return next_node

    def solution(self):
        """
        returns a list of actions to reach thin node 'state'
        """
        return [node.action for node in self.path()[1:]]

    def path(self):
        """
        returns a list of node from root to current node.
        """
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
    """
    Problem of eating one dot on the grid.
    """

    def __init__(self, initial, goal=[], grid=[]):
        Problem.__init__(self, initial, goal)
        self.grid = grid

    def actions(self, state):
        """
        returns all the possible actions from the given state.
        """
        cell = state.cell
        possible_acts = ["UP", "DOWN", "RIGHT", "LEFT"]
        if cell.i == 0 or self.grid[cell.j][cell.i-1].isWall:
            possible_acts.remove("LEFT")
        if cell.j == 0 or self.grid[cell.j-1][cell.i].isWall:
            possible_acts.remove("UP")
        if cell.i == column_cells-1 or self.grid[cell.j][cell.i+1].isWall:
            possible_acts.remove("RIGHT")
        if cell.j == row_cells-1 or self.grid[cell.j+1][cell.i].isWall:
            possible_acts.remove("DOWN")
        return possible_acts

    def goal_test(self, state):
        return state.targets == self.goal

    def result(self, state, action):
        """
        returns the result state from the given state using the given action.
        """
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

    def step_cost(self, current_cost, fRom, action, to):
        """
        cost to from 'fRom' to 'to' with the 'action'
        """
        return current_cost + to.cell.weight

    def h(self, node):
        """
        heuristic to be used in a-star search.
        """
        if len(node.state.targets) > 0:
            a = node.state.cell
            b = node.state.targets[0]
            return node.path_cost + (abs(a.i-b.i) + abs(a.j-b.j))
        else:
            return 0


class State:
    """
    Each state contain a 'cell' and current 'targets' list
    """

    def __init__(self, cell, targets=[]):
        self.cell = cell
        self.targets = targets

    def __eq__(self, value):
        return self.cell == value.cell and self.targets == value.targets

    def __hash__(self):
        return hash((self.cell, frozenset(self.targets)))

    def __repr__(self):
        return "{},{}".format(self.cell, self.targets)


class AllDotsProblem(OneDotProblem):
    """
    Problem of eating 'All the dots' on the grid.
    """

    def __init__(self, initial, goal=[], grid=[]):
        OneDotProblem.__init__(self, initial, goal=goal, grid=grid)
        # dict contains best path cost between each two point
        self.dotsDict = dict()
        for food in initial.targets:
            for tofood in initial.targets:
                self.calcDist2(food, tofood)

    def calcDist2(self, a, b):
        """
        returns the 'best path cost' between point 'a' and 'b' on the grid.
        using a-star search.
        """
        if (a, b) in self.dotsDict:
            return self.dotsDict[a, b]
        prob = OneDotProblem(initial=State(a, [b]), grid=self.grid)
        from core.algorithms import astar
        answer, steps = astar(prob)
        if answer:
            self.dotsDict[a, b] = answer.path_cost
            self.dotsDict[b, a] = answer.path_cost
            return answer.path_cost
        else:
            self.dotsDict[a, b] = 0
            self.dotsDict[b, a] = 0
            return 0

    def h(self, node):
        """
        heuristic to be used in a-star search
        """
        distances = []
        distances_food = []
        for food in node.state.targets:
            for tofood in node.state.targets:
                distances_food.append(
                    (food, tofood, self.calcDist2(food, tofood)))
        if len(distances_food):
            c = max(distances_food, key=lambda a: a[2])
            a, b, x = c
            distances.append(self.calcDist2(node.state.cell, a))
            distances.append(self.calcDist2(node.state.cell, b))
            if len(distances):
                y = min(distances)
            else:
                y = 0
        else:
            x = 0
            y = 0
        return x + y
