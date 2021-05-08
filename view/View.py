import pygame
from model import model
from colors import *

FPS = 60


class View:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((900, 500))
        self.win.fill(WHITE)
        self.small_font = pygame.font.SysFont('Corbel', 35)
        pygame.display.set_caption("Simon Says")

    def show_window(self, squares):
        """Squares to show on the screen"""
        for square in squares:
            self.show_square(square)

    def show_square(self, square):
        """Show on square"""
        rect = self.get_rect_from_square(square)
        pygame.draw.rect(self.win, square.color, rect)
        if isinstance(square, model.Button):
            if square.text is not None:
                text = self.small_font.render(square.text, True, GREEN)
                self.win.blit(text, (square.text_positionX, square.text_positionY))
        pygame.display.update()

    def get_rect_from_square(self, square):
        return pygame.Rect(square.position[0], square.position[1], square.width, square.height)
