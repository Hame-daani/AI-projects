from .difinitions import Problem, Node


def graph_search(problem, frontier, explored, fn):
    # failure check
    if not frontier:
        return None, "failure"

    else:
        # choosing
        if fn == 'popleft':
            node = frontier.pop(0)
        elif fn == 'pop':
            node = frontier.pop(-1)

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


def depth_limited_search(problem, frontier, explored, limit):
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node, 'done'
        elif limit == 0:
            return node, 'cutoff'
        else:
            cutoff_occured = False
            blue = color(0, 0, 255)
            node.state.cell.show(blue)
            for action in problem.actions(node.state):
                child = node.child_node(problem, action)
                n, result = recursive_dls(child, problem, limit-1)
                if result == 'cutoff':
                    cutoff_occured = True
                elif result != 'failure':
                    return n, result
            if cutoff_occured:
                return node, 'cutoff'
            else:
                return None, 'failure'
    # main func
    return recursive_dls(Node(problem.initial_state), problem, limit)


def breadth_fs(problem, frontier, explored):
    node, result = graph_search(problem, frontier, explored, fn="popleft")
    return node, result


def depth_fs(problem, frontier, explored):
    node, result = graph_search(problem, frontier, explored, fn="pop")
    return node, result


def astar(problem, frontier, explored):
    node, result = best_fs(problem, frontier, explored, frontier.f)
    return node, result


def uniform_cost_search(problem, frontier, explored):
    node, result = best_fs(problem, frontier, explored, frontier.f)
    return node, result


def iterative_deeping_search(problem, frontier, explored, depth=[0]):
    depth[0] += 1
    print(str(depth[0])+'\r')
    node, result = depth_limited_search(problem, frontier, explored, depth[0])
    return node, result
