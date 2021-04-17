import pygame
from model import *
from colors import *


FPS = 60


class View:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((900, 500))
        self.win.fill(WHITE)
        pygame.display.set_caption("Simon Says")

    def show_window(self, squares):
        """Squares to show on the screen"""
        for square in squares:
            self.show_square(square)

    def show_square(self, square):
        """Show on square"""
        pygame.draw.rect(self.win, square.color, square.get_rect)
        pygame.display.update()
