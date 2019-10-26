from random import uniform, randint

startImg = loadImage("res/pacman.png")
# color for text
black = color(0, 0, 0)


class Cell(object):
    """
    Cell class used as our enviroment to explore and visualize.
    """
    def __init__(self, i, j, d):
        self.i = i  # x cordinate
        self.j = j  # y cordinate
        self.size = d  # size of cell to be drawn
        self.isWall = False
        self.isStart = False
        self.isEnd = False
        self.weight = randint(1, 10)
        # make 20 percent of cells wall
        if uniform(0, 1) < 0.3:
            self.isWall = True

    def __repr__(self):
        return "({},{})".format(self.i, self.j)

    def show(self, color):
        """
        draw our cell on the display. at it's 'i' and 'j'.
        """
        fill(color)
        noStroke()
        if self.isStart:
            global startImg
            image(startImg, self.i*self.size, self.j *
                  self.size, self.size-1, self.size-1)
        elif self.isEnd:
            circle(self.i*self.size+self.size/2, self.j *
                   self.size+self.size/2, self.size/2)
        else:
            rect(self.i*self.size, self.j*self.size, self.size-1, self.size-1)
        fill(black)
        textSize(self.size/5)
        if self.weight:
            text(self.weight, self.i*self.size+self.size/3,
                 self.j*self.size+self.size/2)

    def makeit(self, what):
        """
        make our cell start or end point.
        """
        if what == 'start':
            self.isStart = True
            self.isEnd = False
        if what == 'end':
            self.isEnd = True
            self.isStart = False
        self.isWall = False
        self.weight = 0
