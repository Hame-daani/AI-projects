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
