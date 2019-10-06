from random import uniform


class Cell(object):
    def __init__(self, i, j, d):
        self.i = i
        self.j = j
        self.isWall = False
        self.explored = False
        self.neighbors = []
        self.previous = None
        self.size = d
        # add walls
        if uniform(0, 1) < 0.2:
            self.isWall = True

    def addNeighbors(self, g, cells):
        i = self.i
        j = self.j
        if i < cells-1:
            self.neighbors.append(g[i+1][j])
        if i > 0:
            self.neighbors.append(g[i-1][j])
        if j < cells-1:
            self.neighbors.append(g[i][j+1])
        if j > 0:
            self.neighbors.append(g[i][j-1])

    def __repr__(self):
        return "({},{})".format(self.i, self.j)

    def show(self, color):
        fill(color)
        noStroke()
        rect(self.i*self.size, self.j*self.size, self.size-1, self.size-1)
