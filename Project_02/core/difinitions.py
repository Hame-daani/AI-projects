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

    def child_node(self, problem: Problem, action):
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
