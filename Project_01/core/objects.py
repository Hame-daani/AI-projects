class Cell(object):
    def __init__(self, i, j, d):
        self.i = i
        self.j = j
        self.isWall = False
        self.explored = False
        self.neighbors = []
        self.previous = None
        self.size = d

    def addNeighbors(self):
        pass

    def __repr__(self):
        return "({},{})".format(self.i, self.j)

    def show(self, color):
        fill(0) if self.isWall else fill(color)
        noStroke()
        rect(self.i*self.size, self.j*self.size, self.size-1, self.size-1)
