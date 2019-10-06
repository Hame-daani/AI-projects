def bfs(frontier, end):
    if len(frontier) == 0:
        return None, "failure"
    else:
        current = frontier.pop()
        if current == end:
            return current, "done"
        current.explored = True
        for n in current.neighbors:
            if not n.explored and not n.isWall:
                n.previous = current
        return current, "pass"
