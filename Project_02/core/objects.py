from random import uniform,randint

startImg = loadImage("res/pacman.png")
black = color(0, 0, 0)

class Cell(object):
    def __init__(self, i, j, d):
        self.i = i
        self.j = j
        self.isWall = False
        self.explored = False
        self.neighbors = []
        self.size = d
        self.isStart = False
        self.isEnd = False
        # add walls
        if uniform(0, 1) < 0.2:
            self.isWall = True
        self.weight = randint(1,10)


    def __repr__(self):
        return "({},{})".format(self.i, self.j)

    def show(self, color):
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
        textSize(self.size/4)
        if self.weight:
            text(self.weight,self.i*self.size+self.size/3,
                    self.j*self.size+self.size/2)

    def makeit(self,what):
        if what == 'start':
            self.isStart = True
            self.isEnd = False
        if what == 'end':
            self.isEnd = True
            self.isStart = False
        self.isWall = False
        self.weight = 0