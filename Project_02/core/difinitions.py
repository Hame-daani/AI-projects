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
