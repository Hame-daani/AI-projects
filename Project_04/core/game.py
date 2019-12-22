import pygame
from core.objects import Board

# A : Ai
# B : Human

block_size = 20
wall_size = 50


class Game:
    def __init__(self, row=10, column=10, width=None, height=None, turn='B'):
        self.marign = 50
        if not width or not height:
            self.width = ((column+1)*block_size) + \
                (column*wall_size)+(self.marign*2)
            self.height = ((row+1)*block_size)+(row*wall_size)+(self.marign*2)
        else:
            self.width = width
            self.height = height
        self.board = Board(row, column, x=self.marign, y=self.marign)
        self.turn = turn
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        # show
        self.screen.fill(255)
        self.board.show(self.screen)
        pygame.display.flip()
        self.last_wall_clicked = None

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
                        r = self.handle_click(x, y)
                        if r:
                            pygame.display.flip()

    def handle_click(self, x, y):
        walls = self.board.get_walls(x, y)
        if not walls or any(wall.taken for wall in walls):
            return False
        if self.last_wall_clicked:
            self.last_wall_clicked.show(self.screen)
        for wall in walls:
            wall.select(self.screen)
            self.last_wall_clicked = wall
        return True
