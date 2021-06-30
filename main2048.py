import pygame
import numpy as np
import random
from constants import CP,TEST_GRID
from pygame.locals import *

N=4

class Game2048:

    #generate 4x4 board
    def __init__(self):
        self.board=np.zeros((N,N),dtype=int)
        self.two_at_random(2)

        self.W = 400
        self.H = self.W
        self.SPACING = 10

        # initialize the pygame module
        pygame.init()

        #title of the screen
        pygame.display.set_caption("2048")

        pygame.font.init()
        self.my_font = pygame.font.SysFont(pygame.font.get_default_font(), 30)

        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode((self.W, self.H))

    # generate 2 at random empty cells
    def two_at_random(self, k=1):
        random_cells = list(zip(*np.where(self.board == 0)))

        for pairs in random.sample(random_cells, k=k):
            self.board[pairs] = 2

    #print board
    def __str__(self):
        return str(self.board)

    #move all non-empty cells to the left row by row
    def place_all_left(self):

        new_board=np.zeros((N,N),dtype=int)
        for i in range(N):
            empty=0

            for j in range(N):
                if(self.board[i][j]!=0):
                    new_board[i][empty]=self.board[i][j]
                    empty+=1

        self.board=new_board

    # merge non-empty cells with same values and make value of merged cell as double
    def merge_cells(self):

        for i in range(N):
            for j in range(N-1):
                if (self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0):
                    self.board[i][j] = self.board[i][j] * 2
                    self.board[i][j + 1] = 0

    # reverse the cells of each row
    def reverse_cells(self):

        new_board = np.zeros((N, N), dtype=int)
        for i in range(N):
            for j in range(N):
                new_board[i][j] = self.board[i][(N-1) - j]

        self.board = new_board

    # interchange rows and columns
    def transpose_board(self):
        for i in range(N):
            for j in range(i + 1, N):
                self.board[i][j], self.board[j][i] = self.board[j][i], self.board[i][j]

    # left move
    def left_move(self):
        self.place_all_left()
        self.merge_cells()
        self.place_all_left()

    # right move
    def right_move(self):
        self.reverse_cells()
        self.left_move()
        self.reverse_cells()

    # move up
    def up_move(self):
        self.transpose_board()
        self.left_move()
        self.transpose_board()

    # move down
    def down_move(self):
        self.transpose_board()
        self.right_move()
        self.transpose_board()

    # win lose or continue
    def game_over(self):

        # if any cell has 2048 then victory
        for i in range(N):
            for j in range(N):
                if (self.board[i][j] == 2048):
                    return 'VICTORY'

        # if any cell is empty then continue game
        for i in range(N):
            for j in range(N):
                if (self.board[i][j] == 0):
                    return 'CONTINUE'

        # Though all cells are not empty but if any adjacent cells are having same values then continue
        for i in range(N-1):
            for j in range(N-1):
                if (self.board[i][j] == self.board[i + 1][j] or self.board[i][j] == self.board[i][j + 1]):
                    return 'CONTINUE'

        for j in range(N-1):
            if (self.board[N-1][j] == self.board[N-1][j + 1] or self.board[j][N-1] == self.board[j + 1][N-1]):
                return 'CONTINUE'

        # if lost
        return 'LOST'

    def win_or_lose(self,game_status):
        status_font=pygame.font.SysFont(pygame.font.get_default_font(),50,False)
        self.screen.fill((CP['back']))
        text = status_font.render(f'{game_status}', True, (0, 0, 0))
        self.screen.blit(text, (130, 130))
        text2 = status_font.render('PRESS "q" to EXIT', True, (0, 0, 0))
        self.screen.blit(text2, (40, 180))


    def show_board(self):
        self.screen.fill(CP['back'])
        rect_w = self.W // N - 2 * self.SPACING
        rect_h = self.H // N - 2 * self.SPACING
        for i in range(N):
            for j in range(N):
                num = self.board[i][j]
                rect_x = j * self.W // N + self.SPACING
                rect_y = i * self.H // N + self.SPACING

                pygame.draw.rect(self.screen, CP[num], pygame.Rect(rect_x, rect_y, rect_w, rect_h), border_radius=9)
                if(num==0):
                    continue
                text_surface = self.my_font.render(f'{num}', True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
                self.screen.blit(text_surface, text_rect)

    @staticmethod
    def wait_for_input():

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 'w'
                    elif event.key == K_LEFT:
                        return 'a'
                    elif event.key == K_DOWN:
                        return 's'
                    elif event.key == K_RIGHT:
                        return 'd'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'q'

    def play(self):

        while True:
            self.show_board()
            pygame.display.flip()
            move = self.wait_for_input()
            # if key == 'q':
            #     print(key)
            #     break

            # print(game_board)
            # print("\n")
            old_game_board = self.board.copy()

            # give input to take move
            # move = input("Take move : ")

            # up move is taken
            if (move == 'W' or move == 'w'):

                # function to take up move is called
                self.up_move()

            # left move is taken
            elif (move == 'A' or move == 'a'):

                # function to take left move is called
                self.left_move()

            # down move is taken
            elif (move == 'S' or move == 's'):

                # function to take down move is called
                self.down_move()

            # right move is taken
            elif (move == 'D' or move == 'd'):

                # function to take right move is called
                self.right_move()

            elif (move == 'Q' or move == 'q'):
                break

            else:
                print("PRESS VALID KEY\n")

            # getting status of the game win lose or continue
            game_status = (self.game_over())

            # print(game_status)
            # print("\n")

            # checking game status
            if (game_status == 'CONTINUE'):
                if all((self.board == old_game_board).flatten()):
                    continue
                self.two_at_random(1)
            else:
                # print(game_status)
                while (True):
                    self.win_or_lose(game_status)
                    pygame.display.flip()
                    move = self.wait_for_input()
                    if (move == 'q'):
                        break
                break


if __name__ == '__main__':
    game=Game2048()
    game.play()


