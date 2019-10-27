from random import uniform, randint

startImg = loadImage("res/pacman.png")
# color for text
black = color(0, 0, 0)


class Cell(object):
    """
    Cell class used as our enviroment to explore and visualize.
    """

    def __init__(self, i, j, w, h):
        self.i = i  # x cordinate
        self.j = j  # y cordinate
        self.w = w
        self.h = h
        self.isWall = False
        self.isStart = False
        self.isEnd = False
        self.weight = 0

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
            image(startImg, self.i*self.w, self.j *
                  self.h, self.w-1, self.h-1)
        elif self.isEnd:
            circle(self.i*self.w+self.w/2, self.j *
                   self.h+self.h/2, self.w/2)
        else:
            rect(self.i*self.w, self.j*self.h, self.w-1, self.h-1)
        fill(black)
        textSize(self.w/5)
        if self.weight:
            text(self.weight, self.i*self.w+self.w/3,
                 self.j*self.h+self.h/2)

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
