from .difinitions import Problem


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


def breadth_fs(problem, frontier, explored):
    node, result = graph_search(problem, frontier, explored, fn="popleft")
    return node, result


def depth_fs(problem, frontier, explored):
    node, result = graph_search(problem, frontier, explored, fn="pop")
    return node, result


def heuristic(a, b):
    return abs(a.i-b.i) + abs(a.j-b.j)


def astar(frontier, end):
    # failure check
    if not frontier:
        return None, "failure"
    else:
        # choose l
        current = None
        for fro in frontier:
            if not current or current.f > fro.f:
                current = fro
        # solution check
        if current == end:
            return current, "done"
        # expand
        current.explored = True
        frontier.remove(current)
        for n in current.neighbors:
            if not n.explored and not n.isWall:
                if n.g > current.g+1:
                    n.previous = current
                    n.g = current.g+1
                    n.f = n.g+heuristic(n, end)
                    if not n in frontier:
                        frontier.append(n)
        return current, "pass"
