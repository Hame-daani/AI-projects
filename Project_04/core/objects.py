import pygame

lineX = pygame.image.load("pics/lineX.png")
lineXempty = pygame.image.load("pics/lineXempty.png")
lineY = pygame.image.load("pics/lineY.png")
lineYempty = pygame.image.load("pics/lineYempty.png")
block = pygame.image.load("pics/block.png")
empty = pygame.image.load("pics/empty.png")
A = pygame.image.load("pics/A.png")
B = pygame.image.load("pics/B.png")

block_size = 4
wall_size = 26


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

    def get_wall(self, x, y):
        return None, None

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
        self.upper_wall = Wall(x=self.x+block_size, y=self.y, upside=False)
        self.bottom_wall = Wall(x=self.x+block_size,
                                y=self.y+block_size+wall_size, upside=False)
        self.left_wall = Wall(x=self.x, y=self.y+block_size, upside=True)
        self.right_wall = Wall(x=self.x+block_size +
                               wall_size, y=self.y+block_size, upside=True)
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
        self.upper_wall.show(screen)
        self.bottom_wall.show(screen)
        self.left_wall.show(screen)
        self.right_wall.show(screen)


class Wall(object):
    def __init__(self, x, y,  upside, taken=False):
        self.upside = upside
        self.taken = taken
        self.x = x
        self.y = y
        super().__init__()

    def show(self, screen):
        if self.taken:
            if self.upside:
                screen.blit(lineY, (self.x, self.y))
            else:
                screen.blit(lineX, (self.x, self.y))
        else:
            if self.upside:
                screen.blit(lineYempty, (self.x, self.y))
            else:
                screen.blit(lineXempty, (self.x, self.y))
