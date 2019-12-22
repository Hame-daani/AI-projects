import pygame

lineX = pygame.image.load("pics/lineX.png")
lineXempty = pygame.image.load("pics/lineXempty.png")
lineY = pygame.image.load("pics/lineY.png")
lineYempty = pygame.image.load("pics/lineYempty.png")
block = pygame.image.load("pics/block.png")
empty = pygame.image.load("pics/empty.png")
A = pygame.image.load("pics/A.png")
B = pygame.image.load("pics/B.png")
last_X = pygame.image.load("pics/last_X.png")
last_Y = pygame.image.load("pics/last_Y.png")

block_size = 20
wall_size = 50


class Board(object):
    def __init__(self, row_num, column_num, x, y):
        self.x = x
        self.y = y
        self.pixle = block_size+wall_size
        self.row_num = row_num
        self.column_num = column_num
        self.grid = [
            [
                Box(row, column, x=self.x+column*self.pixle, y=self.y+row*self.pixle) for column in range(column_num)
            ]
            for row in range(row_num)
        ]
        super().__init__()

    def get_walls(self, x, y):
        walls = []
        for row in self.grid:
            for box in row:
                for wall in box.walls:
                    if wall.trigred(x, y):
                        walls.append(wall)
        return walls

    def show(self, screen):
        for row in self.grid:
            for box in row:
                box.show(screen)


class Box(object):
    def __init__(self, row, column, x, y, taken=None):
        self.x = x
        self.y = y
        self.row = row
        self.column = column
        self.taken = taken
        self.walls = [
            RightWall(self, x=self.x+block_size + wall_size,
                      y=self.y+block_size),
            BottomWall(self, x=self.x+block_size,
                       y=self.y+block_size+wall_size),
            LeftWall(self, x=self.x, y=self.y+block_size),
            UpperWall(self, x=self.x+block_size, y=self.y),
        ]
        super().__init__()

    def show(self, screen):
        x, y = self.x, self.y
        screen.blit(block, (x, y))
        x, y = self.x+block_size+wall_size, self.y
        screen.blit(block, (x, y))
        x, y = self.x, self.y+block_size+wall_size
        screen.blit(block, (x, y))
        x, y = self.x+block_size+wall_size, self.y+block_size+wall_size
        screen.blit(block, (x, y))
        x, y = self.x+block_size, self.y+block_size
        if not self.taken:
            screen.blit(empty, (x, y))
        elif self.taken == 'A':
            screen.blit(A, (x, y))
        elif self.taken == 'B':
            screen.blit(B, (x, y))
        for wall in self.walls:
            wall.show(screen)

    def get_wall(self, x, y):
        if self.upper_wall.trigred(x, y):
            return self.upper_wall
        if self.bottom_wall.trigred(x, y):
            return self.bottom_wall
        if self.left_wall.trigred(x, y):
            return self.left_wall
        if self.right_wall.trigred(x, y):
            return self.right_wall


class Wall(object):
    def __init__(self, box, x, y, taken=False):
        self.box = box
        self.taken = taken
        self.x = x
        self.y = y
        super().__init__()

    def show(self, screen):
        raise NotImplementedError

    def trigred(self, x, y):
        raise NotImplementedError

    def select(self, screen):
        raise NotImplementedError

    def __repr__(self):
        return f"({self.box.row+1},{self.box.column+1})"


class RightWall(Wall):
    def __init__(self, box, x, y, taken=False):
        super().__init__(box, x, y, taken=taken)

    def show(self, screen):
        if self.taken:
            screen.blit(lineY, (self.x, self.y))
        else:
            screen.blit(lineYempty, (self.x, self.y))

    def select(self, screen):
        screen.blit(last_Y, (self.x, self.y))
        self.taken = True

    def __repr__(self):
        return super().__repr__()+"Right"

    def trigred(self, x, y):
        if x >= self.x and x <= self.x+block_size:
            if y >= self.y and y <= self.y+wall_size:
                return True
        return False


class LeftWall(Wall):
    def __init__(self, box, x, y, taken=False):
        super().__init__(box, x, y, taken=taken)

    def show(self, screen):
        if self.taken:
            screen.blit(lineY, (self.x, self.y))
        else:
            screen.blit(lineYempty, (self.x, self.y))

    def select(self, screen):
        screen.blit(last_Y, (self.x, self.y))
        self.taken = True

    def __repr__(self):
        return super().__repr__()+"Left"

    def trigred(self, x, y):
        if x >= self.x and x <= self.x+block_size:
            if y >= self.y and y <= self.y+wall_size:
                return True
        return False


class UpperWall(Wall):
    def __init__(self, box, x, y, taken=False):
        super().__init__(box, x, y, taken=taken)

    def show(self, screen):
        if self.taken:
            screen.blit(lineX, (self.x, self.y))
        else:
            screen.blit(lineXempty, (self.x, self.y))

    def __repr__(self):
        return super().__repr__()+"Upper"

    def select(self, screen):
        screen.blit(last_X, (self.x, self.y))
        self.taken = True

    def trigred(self, x, y):
        if x >= self.x and x <= self.x+wall_size:
            if y >= self.y and y <= self.y+block_size:
                return True
        return False


class BottomWall(Wall):
    def __init__(self, box, x, y, taken=False):
        super().__init__(box, x, y, taken=taken)

    def show(self, screen):
        if self.taken:
            screen.blit(lineX, (self.x, self.y))
        else:
            screen.blit(lineXempty, (self.x, self.y))

    def __repr__(self):
        return super().__repr__()+"Bottom"

    def select(self, screen):
        screen.blit(last_X, (self.x, self.y))
        self.taken = True

    def trigred(self, x, y):
        if x >= self.x and x <= self.x+wall_size:
            if y >= self.y and y <= self.y+block_size:
                return True
        return False
