import pygame
from core.objects import Board

# A : Ai
# B : Human


class Game:
    def __init__(self, row=5, column=5, width=None, height=None, turn='B'):
        if not width or not height:
            self.width = column*40
            self.height = row*40
        else:
            self.width = width
            self.height = height
        self.marign = self.height*0.07
        self.board = Board(row, column, x=self.marign, y=self.marign)
        self.turn = turn
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.screen.fill(255)
        self.show()

    def show(self):
        self.board.show(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            if self.turn == 'A':
                # ai turn
                pass
            else:
                # human turn
                for event in pygame.event.get():
                    # quit the game when the player closes it
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                    # left click
                    elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        # get the current position of the cursor
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]

                        # valid_x = self.width-self.marign
                        # valid_y = self.height-self.marign
                        # if x < valid_x or y < valid_y:
                        #     continue
                        # valid_x = self.width-self.marign
                        # valid_y = self.height-self.marign

                        # check whether it was a not set wall that was clicked
                        wall1, wall2 = self.board.get_wall(x, y)
                        if not wall1:
                            # invalid click
                            continue
                        if not wall2:
                            # upper or side walls
                            pass
                        wall_x, wall_y = self.get_wall(x, y)
