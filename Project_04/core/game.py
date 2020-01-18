from collections.abc import Iterable

import pygame
from core.algorithm import alpha_beta_search, iterative_alpha_beta_search
from core.objects import Board

# A : Ai
# H : Human

block_size = 20
wall_size = 50


class Game:
    def __init__(self, row=4, column=4, width=None, height=None, turn='H'):
        self.marign = 50
        if not width or not height:
            self.width = ((column+1)*block_size) + \
                (column*wall_size)+(self.marign*2)
            self.height = ((row+1)*block_size)+(row*wall_size)+(self.marign*2)
        else:
            self.width = width
            self.height = height
        self.board = Board(row, column, x=self.marign,
                           y=self.marign, turn=turn)
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        # show
        self.screen.fill(255)
        self.board.show(self.screen)
        pygame.display.flip()
        self.last_wall_clicked = None

    def run(self):
        while not self.board.won():
            move = None
            if self.board.turn == 'A':
                # ai turn
                move = iterative_alpha_beta_search(self.board)
            else:
                # human turn
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                    elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]
                        move = self.handle_click(x, y)
            if move:
                self.play_the_move(move)
                pygame.display.set_caption(
                    f"Turn:{self.board.turn}  A:{self.board.boxes['A']}     H:{self.board.boxes['H']}")
                pygame.display.flip()
        # after while
        # finish
        print(f"A:{self.board.boxes['A']} H:{self.board.boxes['H']}")

    def handle_click(self, x, y):
        walls = self.board.get_walls(x, y)
        if not walls or any(wall.taken for wall in walls):
            return None
        return walls

    def play_the_move(self, move):
        if not isinstance(move, Iterable):
            move = [move]
        if self.last_wall_clicked:
            self.last_wall_clicked.show(self.screen)
        self.board.do_move(move)
        if not isinstance(move, Iterable):
            move = [move]
        for wall in move:
            if wall.box.taken:
                wall.box.show(self.screen)
            wall.show(self.screen, last=True)
            self.last_wall_clicked = wall
