class Cell(object):
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.isWall = False
        self.explored = False
        self.neighbors = []
        self.previous = None

    def addNeighbors(self):
        pass
