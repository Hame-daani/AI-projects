from .difinitions import Problem, Node
from core.utils import PriorityQueue


def graph_search(problem, fn):
    """
    base function to be used in breadth first
    and depth first search.
    """
    frontier = [Node(problem.initial_state)]
    explored = set()
    # visualize purpose
    steps = []
    while frontier:
        # choosing
        if fn == 'popleft':
            node = frontier.pop(0)
        elif fn == 'pop':
            node = frontier.pop(-1)
        # visualize purpose
        steps.append((node, frontier[:], explored.copy()))
        # explore
        explored.add(node.state)
        # expand
        for action in problem.actions(node.state):
            child = node.child_node(problem, action)
            if child.state not in explored and child not in frontier:
                # goal check
                if problem.goal_test(child.state):
                    return child, steps
                frontier.append(child)
    # failure
    return None, steps


def best_fs(problem, fn):
    """
    base function to be used in a-satr and
    unifrom cost search.
    """
    frontier = PriorityQueue('min', fn)
    frontier.append(Node(problem.initial_state))
    explored = set()
    # visualize purpose
    steps = []
    while frontier:
        # choosing
        node = frontier.pop()
        # goal check
        if problem.goal_test(node.state):
            return node, steps
        # visualize purpose
        steps.append((node, frontier.copy(), explored.copy()))
        # explore
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
    # failure check
    return None, steps


# def depth_limited_search(problem, frontier, explored, limit):
#     def recursive_dls(node, problem, limit):
#         if problem.goal_test(node.state):
#             return node, 'done'
#         elif limit == 0:
#             return node, 'cutoff'
#         else:
#             cutoff_occured = False
#             blue = color(0, 0, 255)
#             node.state.cell.show(blue)
#             for action in problem.actions(node.state):
#                 child = node.child_node(problem, action)
#                 n, result = recursive_dls(child, problem, limit-1)
#                 if result == 'cutoff':
#                     cutoff_occured = True
#                 elif result != 'failure':
#                     return n, result
#             if cutoff_occured:
#                 return node, 'cutoff'
#             else:
#                 return None, 'failure'
#     # main func
#     return recursive_dls(Node(problem.initial_state), problem, limit)


def breadth_fs(problem):
    node, steps = graph_search(problem, fn="popleft")
    return node, steps


def depth_fs(problem):
    node, steps = graph_search(problem, fn="pop")
    return node, steps


def astar(problem):
    node, steps = best_fs(problem, lambda n: n.path_cost+problem.h(n))
    return node, steps


def uniform_cost_search(problem):
    node, steps = best_fs(problem, lambda n: n.path_cost)
    return node, steps


# def iterative_deeping_search(problem, frontier, explored, depth=[0]):
#     depth[0] += 1
#     print(str(depth[0])+'\r')
#     node, result = depth_limited_search(problem, frontier, explored, depth[0])
#     return node, result
