from .difinitions import Problem, PriorityQueue, Node


def graph_search(problem, frontier, explored, fn):
    # failure check
    if not frontier:
        return None, "failure"

    else:
        # choosing
        if fn == 'popleft':
            node = frontier.pop(0)
        elif fn == 'pop':
            node = frontier.pop()

        explored.add(node.state)
        # expand
        for action in problem.actions(node.state):
            child = node.child_node(problem, action)
            if child.state not in explored and child not in frontier:
                # goal check
                if problem.goal_test(child.state):
                    return child, "done"
                frontier.append(child)
        return node, "pass"


def best_fs(problem, frontier, explored, fn):
    # failure check
    if not frontier:
        return None, "failure"
    else:
        # choosing
        node = frontier.pop()
        # goal check
        if problem.goal_test(node.state):
            return node, "done"
        explored.add(node.state)
        # expand
        for action in problem.actions(node.state):
            child = node.child_node(problem, action)
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if fn(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
        return node, "pass"


def breadth_fs(problem, frontier, explored):
    node, result = graph_search(problem, frontier, explored, fn="popleft")
    return node, result


def depth_fs(problem, frontier, explored):
    node, result = graph_search(problem, frontier, explored, fn="pop")
    return node, result


def astar(problem, frontier, explored):
    node, result = best_fs(problem, frontier, explored,
                           lambda n: n.path_cost+problem.h(n))
    return node, result


def uniform_cost_search(problem, frontier, explored):
    node, result = best_fs(problem, frontier, explored, lambda n: n.path_cost)
    return node, result
