import heapq


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
        if cell.i == len(self.grid)-1 or self.grid[cell.j][cell.i+1].isWall:
            possible_acts.remove("RIGHT")
        if cell.j == len(self.grid)-1 or self.grid[cell.j+1][cell.i].isWall:
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
        self.dotsDict = dict()  # dict contains best path cost between each two target
        self.calcDotsDistDict()

    def calcDist2(self, a, b):
        """
        returns the 'best path cost' between point 'a' and 'b' on the grid.
        using a-star search.
        """
        prob = OneDotProblem(initial=State(a, [b]), grid=self.grid)
        frontier = PriorityQueue('min', prob.h)
        explored = set()
        frontier.append(Node(state=prob.initial_state))
        from core.algorithms import astar
        while frontier:
            node, result = astar(prob, frontier, explored)
            if result == "done":
                return node.path_cost
            elif result == "failure":
                print("Error dist 2: ",a,b)
                return 0

    def calcDotsDistDict(self):
        """
        Fill our dotsDict to be used in heuristic.
        """
        for a in self.initial_state.targets:
            for b in self.initial_state.targets:
                if not a == b:
                    if (b, a) in self.dotsDict:
                        self.dotsDict[a, b] = self.dotsDict[b, a]
                    else:
                        self.dotsDict[a, b] = self.calcDist2(a, b)
                        if not self.dotsDict[a, b] or self.dotsDict[a, b] == 0:
                            print("Error calc dict: ",a,b)

    def h(self, node):
        """
        heuristic to be used in a-star search
        """
        # https://stackoverflow.com/questions/9994913/pacman-what-kinds-of-heuristics-are-mainly-used
        def dist_two_furthest_dots():
            """
            return the distance between two furthest dots
            """
            keys = self.dotsDict.keys()
            valids = list(
                set([i for k in keys for i in k])
                &
                set(node.state.targets)
            )
            l = []
            for key in self.dotsDict.keys():
                a, b = key
                if a in valids and b in valids:
                    l.append(self.dotsDict.get(key))
            m = max(l)
            if m == 0:
                print("Error two furtehst: ", keys, valids)
            return m

        # second function
        def curr_pos_to_close_two(x):
            """
            returns distance from pacman to closest of two dot
            """
            for k, v in self.dotsDict.items():
                if v == x:
                    a, b = k
                    dist_to1 = self.calcDist2(a, node.state.cell)
                    dist_to2 = self.calcDist2(b, node.state.cell)
                    m = min([dist_to1, dist_to2])
                    if m == 0 or not m:
                        print("Error curr to close: ",a,b)
                    return m
        # h function
        if len(node.state.targets) == 1:
            return super(AllDotsProblem, self).h(node)
        elif len(node.state.targets) != 0:
            x = dist_two_furthest_dots()
            y = curr_pos_to_close_two(x)
            return x + y
        else:
            return 0


class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        self.current = -1

        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __iter__(self):
        return self

    def next(self):
        self.current += 1
        if self.current < len(self.heap):
            return self.heap[self.current]
        self.current = -1
        raise StopIteration

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)
