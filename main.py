import pygame
import random
from pygame.locals import *
import numpy as np
import sys
import os
from datetime import datetime


CP = {
    'back': (189, 172, 161),
    0: (204, 192, 179),
    2: (238, 228, 219),
    4: (240, 226, 202),
    8: (242, 177, 121),
    16: (236, 141, 85),
    32: (250, 123, 92),
    64: (234, 90, 56),
    128: (237, 207, 114),
    256: (242, 208, 75),
    512: (237, 200, 80),
    1024: (227, 186, 19),
    2048: (236, 196, 2),
    4096: (96, 217, 146)
}
TEST_GRID = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 4096],
                      [0, 0, 0, 0]])

N = 4
W = 400
H = 600
SPACING = 10
score = 0


class G2048():
    def __init__(self):
        self.Grid = np.zeros((N, N), dtype=int)
        pygame.init()
        pygame.display.set_caption("2048")
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Arial', 30)
        self.screen = pygame.display.set_mode((W, H))

    
    def __str__(self):
        return str(self.Grid)


    def add_number(self, k=1):
        empty = list(zip(*np.where(self.Grid==0)))
        for i in random.sample(empty, k=k):
            self.Grid[i] = random.choice([2, 4])


    def save_result(self):
        with open(f'D:\Projects\Project 2048\{datetime.now().strftime("%H-%M-%S")}.txt', 'w') as f:
            f.write('----------\n')
            for i in self.Grid:
                f.write(f'{i}\n')
            f.write('----------\n')
            f.write(f'Your score is {score}')
        f.close()

    
    @staticmethod
    def double_it(dll):
        global score
        dll_n = dll[dll != 0]
        dll_n_sum = []
        skip = False
        for j in range(len(dll_n)):
            if skip:
                skip = False
                continue
            if j != len(dll_n) - 1 and dll_n[j] == dll_n[j + 1]:
                upd_n = dll_n[j] * 2
                score += dll_n[j] * 2
                skip = True
            else:
                upd_n = dll_n[j]
            dll_n_sum.append(upd_n)
        return np.array(dll_n_sum)

    
    def make_move(self, move):
        for i in range(N):
            if move in 'lr':
                dll = self.Grid[i, :]
            else:
                dll = self.Grid[:, i]
            tr = False
            if move in 'rd':
                tr = True
                dll = dll[::-1]
            dll_n = self.double_it(dll)
            upd_dll = np.zeros_like(dll)
            upd_dll[:len(dll_n)] = dll_n
            if tr:
                upd_dll = upd_dll[::-1]

            if move in 'lr':
                self.Grid[i, :] = upd_dll
            else:
                self.Grid[:, i] = upd_dll


    def main_game(self):
        self.add_number()
        while True:
            self.draw_game()
            pygame.display.flip()
            cmd = self.wait_for_key()
            if cmd == 'q':
                break
            old_Grid = self.Grid.copy()
            self.make_move(cmd)
            if self.over():
               self.save_result()
               break
            if not all((self.Grid == old_Grid).flatten()):
                self.add_number()
            


    def draw_game(self):
        self.screen.fill(CP['back'])
        for i in range(N):
            for j in range(N):
                n = self.Grid[i][j]
                rect_x = j * W // N + SPACING
                rect_y = i * H // N + SPACING
                rect_w = W // N - 2 * SPACING
                rect_h = H // N - 2 * SPACING
                pygame.draw.rect(self.screen,
                                CP[n],
                                pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                                border_radius=8)
                if n == 0:
                    continue
                text_surface = self.myfont.render(f'{n}', True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(rect_x + rect_w/2,
                                                        rect_y + rect_h/2))
                self.screen.blit(text_surface, text_rect)

    
    def over(self):
        Grid_bu = self.Grid.copy()
        for move in 'lrud':
            self.make_move(move)
            if not all((self.Grid == Grid_bu).flatten()):
                self.Grid = Grid_bu
                return False
        return True
    

    @staticmethod
    def wait_for_key():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'q'
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 'u'
                    elif event.key == K_RIGHT:
                        return 'r'
                    elif event.key == K_LEFT:
                        return 'l'
                    elif event.key == K_DOWN:
                        return 'd'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'q'


if __name__ == '__main__':
    game = G2048()
    game.main_game()