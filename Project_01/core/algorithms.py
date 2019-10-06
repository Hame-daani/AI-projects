def bfs(frontier, end):
    # failure check
    if len(frontier) == 0:
        return None, "failure"
    else:
        # choose l
        current = frontier.pop(0)
        # solution check
        if current == end:
            return current, "done"
        # expend
        current.explored = True
        for n in current.neighbors:
            if not n.explored and not n.isWall and not frontier.count(n):
                n.previous = current
                frontier.append(n)
        return current, "pass"


def dfs(frontier, end):
    # failure check
    if len(frontier) == 0:
        return None, "failure"
    else:
        # choose l
        current = frontier.pop()
        # solution check
        if current == end:
            return current, "done"
        # expend
        current.explored = True
        for n in current.neighbors:
            if not n.explored and not n.isWall and not frontier.count(n):
                n.previous = current
                frontier.append(n)
        return current, "pass"


def heuristic(a, b):
    import math
    # return math.sqrt((a.i-b.i)**2 + (a.j-b.j)**2)
    return abs(a.i-b.i) + abs(a.j-b.j)


def astar(frontier, end):
    if len(frontier) == 0:
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
        # expend
        frontier.remove(current)
        current.explored = True
        for n in current.neighbors:
            if not n.explored and not n.isWall:
                if n.g > current.g+1:
                    n.previous = current
                    n.g = current.g+1
                    n.f = n.g+heuristic(n, end)
                    if not frontier.count(n):
                        frontier.append(n)
        return current, "pass"
