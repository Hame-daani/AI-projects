from collections.abc import Iterable
from copy import deepcopy

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
    def __init__(self, row_num, column_num, x, y, turn):
        self.x = x
        self.y = y
        self.turn = turn
        self.pixle = block_size+wall_size
        self.row_num = row_num
        self.column_num = column_num
        self.boxes = {'A': 0, 'H': 0}
        self.grid = [
            [
                Box(self, row, column, x=self.x+column*self.pixle, y=self.y+row*self.pixle) for column in range(column_num)
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

    def do_move(self, move=None):
        if not move:
            return
        swap = True
        if not isinstance(move, Iterable):
            move = [move]
        for wall in move:
            wall.taken = True
            if wall.box.isComplete():
                wall.box.taken = self.turn
                self.boxes[self.turn] += 1
                swap = False
        if swap:
            self.swap_turn()
    
    def undo_move(self, move=None):
        if not move:
            return
        swap = True
        if not isinstance(move, Iterable):
            move = [move]
        for wall in move:
            if wall.box.isComplete():
                wall.box.taken = None
                self.boxes[self.turn] -= 1
                swap = False
            wall.taken = False
        if swap:
            self.swap_turn()


    def utility(self,move=None):
        self.do_move(move)
        util = self.boxes['A'] - self.boxes['H']
        self.undo_move(move)
        return util

    def swap_turn(self):
        self.turn = 'A' if self.turn == 'H' else 'H'

    def won(self):
        row = self.row_num
        column = self.column_num
        a_boxes = self.boxes['A']
        h_boxes = self.boxes['H']
        return (row*column) == (a_boxes+h_boxes)

    def isTerminal(self):
        return self.won()

    def actions(self):
        moves = set()
        R = 0
        B = 1
        L = 2
        U = 3
        for row in self.grid:
            for box in row:
                for wall in box.walls:
                    if not wall.taken:
                        # up
                        if isinstance(wall, UpperWall):
                            if wall.box.row == 0:
                                moves.add(frozenset([wall]))
                            else:
                                i = wall.box.row
                                j = wall.box.column
                                moves.add(frozenset([wall, self.grid[i-1][j].walls[B]]))
                        # bottom
                        elif isinstance(wall, BottomWall):
                            if wall.box.row == wall.box.board.row_num-1:
                                moves.add((wall))
                            else:
                                i = wall.box.row
                                j = wall.box.column
                                moves.add(frozenset([wall, self.grid[i+1][j].walls[U]]))
                        # right
                        elif isinstance(wall, RightWall):
                            if wall.box.column == wall.box.board.column_num-1:
                                moves.add(frozenset([wall]))
                            else:
                                i = wall.box.row
                                j = wall.box.column
                                moves.add(frozenset([wall, self.grid[i][j+1].walls[L]]))
                        # left
                        elif isinstance(wall, LeftWall):
                            if wall.box.column == 0:
                                moves.add(frozenset([wall]))
                            else:
                                i = wall.box.row
                                j = wall.box.column
                                moves.add(frozenset([wall, self.grid[i][j-1].walls[R]]))
        return sorted(moves,key=self.utility)


class Box(object):
    def __init__(self, board, row, column, x, y, taken=None):
        self.board = board
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

    def isComplete(self):
        return all(wall.taken for wall in self.walls)

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
        elif self.taken == 'H':
            screen.blit(B, (x, y))
        for wall in self.walls:
            wall.show(screen)


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
        return f"({self.box.row},{self.box.column})"


class RightWall(Wall):
    def __init__(self, box, x, y, taken=False):
        super().__init__(box, x, y, taken=taken)

    def show(self, screen, last=False):
        if self.taken:
            if last:
                screen.blit(last_Y, (self.x, self.y))
            else:
                screen.blit(lineY, (self.x, self.y))
        else:
            screen.blit(lineYempty, (self.x, self.y))

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

    def show(self, screen, last=False):
        if self.taken:
            if last:
                screen.blit(last_Y, (self.x, self.y))
            else:
                screen.blit(lineY, (self.x, self.y))
        else:
            screen.blit(lineYempty, (self.x, self.y))

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

    def show(self, screen, last=False):
        if self.taken:
            if last:
                screen.blit(last_X, (self.x, self.y))
            else:
                screen.blit(lineX, (self.x, self.y))
        else:
            screen.blit(lineXempty, (self.x, self.y))

    def __repr__(self):
        return super().__repr__()+"Upper"

    def trigred(self, x, y):
        if x >= self.x and x <= self.x+wall_size:
            if y >= self.y and y <= self.y+block_size:
                return True
        return False


class BottomWall(Wall):
    def __init__(self, box, x, y, taken=False):
        super().__init__(box, x, y, taken=taken)

    def show(self, screen, last=False):
        if self.taken:
            if last:
                screen.blit(last_X, (self.x, self.y))
            else:
                screen.blit(lineX, (self.x, self.y))
        else:
            screen.blit(lineXempty, (self.x, self.y))

    def __repr__(self):
        return super().__repr__()+"Bottom"

    def trigred(self, x, y):
        if x >= self.x and x <= self.x+wall_size:
            if y >= self.y and y <= self.y+block_size:
                return True
        return False
